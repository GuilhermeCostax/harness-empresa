#!/usr/bin/env python3
"""Hooks do harness: bloqueiam o que as regras gerais proíbem, em vez de só pedir.

Uso (chamado pelo hooks/hooks.json, com o JSON do Claude Code no stdin):
  harness_hooks.py pre-bash    antes de um comando Bash: bloqueia o que é perigoso
  harness_hooks.py post-bash   depois de um commit: confere a mensagem e a documentação

Sair com código 2 bloqueia o comando (pre) ou devolve o aviso ao Claude (post); o texto vai no
stderr. Qualquer outro erro do próprio hook sai com 0 para não travar o trabalho do dev.

A configuração de cada projeto fica em <projeto>/.claude/harness.json (ver INSTALAR.md). Sem o
arquivo, só valem as checagens que não dependem do projeto.
"""
import json
import os
import re
import subprocess
import sys
import time
from urllib.parse import urlparse

HOSTS_LOCAIS_PADRAO = ["localhost", "127.0.0.1", "::1", "0.0.0.0", "host.docker.internal"]
ASSINATURAS_CLAUDE = [
    r"co-authored-by:\s*claude",
    r"noreply@anthropic\.com",
    r"generated with \[?claude code",
]


def sh(args, cwd):
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def raiz_do_projeto(entrada):
    cwd = entrada.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    return sh(["git", "rev-parse", "--show-toplevel"], cwd) or cwd, cwd


def ler_config(raiz):
    try:
        with open(os.path.join(raiz, ".claude", "harness.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def branch_principal(raiz, config):
    if config.get("branchPrincipal"):
        return config["branchPrincipal"]
    ref = sh(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], raiz)
    return ref.split("/", 1)[1] if "/" in ref else "main"


def limpar_comando(comando):
    """Tira corpo de heredoc e texto entre aspas, para uma mensagem de commit que *fala* de
    `git reset --hard` não ser confundida com o comando."""
    linhas, saida, fim = comando.split("\n"), [], None
    for linha in linhas:
        if fim is not None:
            if linha.strip() == fim:
                fim = None
            continue
        m = re.search(r"<<-?\s*['\"]?(\w+)['\"]?", linha)
        if m:
            fim = m.group(1)
        saida.append(linha)
    texto = "\n".join(saida)
    texto = re.sub(r'"(?:\\.|[^"\\])*"', '""', texto)
    texto = re.sub(r"'[^']*'", "''", texto)
    return texto


def partes(comando):
    return [p.strip() for p in re.split(r"&&|\|\||;|\n|\|", comando) if p.strip()]


def bloquear(motivo):
    print(f"[harness] Bloqueado: {motivo}", file=sys.stderr)
    sys.exit(2)


# ---------- pre-bash ----------

def checar_git(parte, raiz, config):
    if re.search(r"\bgit\b.*\breset\b.*--hard\b", parte):
        bloquear(
            "`git reset --hard` apaga trabalho sem volta. Para resolver conflito, mantenha as duas "
            "alterações; se precisar mesmo descartar algo, peça ao dev para rodar ele mesmo."
        )
    if not re.search(r"\bgit\b(\s+-\S+)*\s+push\b", parte):
        return
    tokens = parte.split()
    depois = tokens[tokens.index("push") + 1:] if "push" in tokens else []
    forca_bruta = any(
        t == "--force" or (re.fullmatch(r"-[a-zA-Z]+", t) and "f" in t) or t.startswith("+")
        for t in depois
    )
    if forca_bruta:
        bloquear(
            "push forçado com `--force`/`-f`/`+refspec`. Na branch da própria tarefa, depois de um "
            "rebase, use `git push --force-with-lease`. Na principal, nunca."
        )
    if any(t.startswith("--force-with-lease") for t in depois):
        principal = branch_principal(raiz, config)
        atual = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], raiz)
        destinos = [t.split(":")[-1] for t in depois if not t.startswith("-")]
        alvo = destinos[1] if len(destinos) > 1 else atual
        if alvo == "HEAD":
            alvo = atual
        if alvo == principal or alvo.endswith("/" + principal):
            bloquear(f"push forçado na branch principal (`{principal}`). Nunca na principal.")


def host_do_valor(valor):
    valor = valor.strip().strip("'\"")
    m = re.search(r"@tcp\(([^:)]*)", valor)  # DSN do Go: user:senha@tcp(host:porta)/banco
    if m:
        return m.group(1)
    if "://" in valor:
        return urlparse(valor).hostname or ""
    return valor.split(":")[0]


def ler_env(caminho):
    valores = {}
    try:
        with open(caminho, encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith("#") and "=" in linha:
                    k, v = linha.split("=", 1)
                    valores[k.strip().removeprefix("export ").strip()] = v.strip()
    except OSError:
        pass
    return valores


def checar_producao(parte, raiz, config):
    prod = config.get("producao")
    if not prod:
        return
    if not any(re.search(r"\b" + re.escape(c) + r"\b", parte) for c in prod.get("comandos", [])):
        return
    env = ler_env(os.path.join(raiz, prod.get("arquivoEnv", ".env")))
    var_ambiente = prod.get("variavelAmbiente")
    if var_ambiente and env.get(var_ambiente, "").strip("'\"").lower() in [
        v.lower() for v in prod.get("valoresProibidos", ["production", "prod"])
    ]:
        bloquear(
            f"`{prod.get('arquivoEnv')}` está com {var_ambiente} de produção. Este comando roda "
            "migrations ou mexe em dados: nunca contra produção."
        )
    locais = prod.get("hostsLocais", HOSTS_LOCAIS_PADRAO)
    for var in prod.get("variaveisDeBanco", []):
        if var in env:
            host = host_do_valor(env[var])
            if host and host not in locais:
                bloquear(
                    f"`{var}` em `{prod.get('arquivoEnv')}` aponta para um banco fora da máquina "
                    f"(host não está em {locais}). Este comando roda migrations ou mexe em dados: "
                    "só no banco de desenvolvimento. Se esse host é de dev, o dev acrescenta em "
                    "`producao.hostsLocais` no `.claude/harness.json`."
                )


def checar_testes_simultaneos(parte, config):
    testes = config.get("testes")
    if not testes:
        return
    if not any(re.search(r"\b" + re.escape(c) + r"\b", parte) for c in testes.get("comandos", [])):
        return
    padrao = testes.get("processoEmExecucao")
    if not padrao:
        return
    r = subprocess.run(["pgrep", "-f", padrao], capture_output=True, text=True)
    pids = [p for p in r.stdout.split() if p and int(p) != os.getpid()]
    if pids:
        bloquear(
            "já tem uma execução de testes rodando nesta máquina (pode ser do dev ou uma da IA em "
            "segundo plano). O banco de teste é um só e duas execuções se apagam no meio. Espere "
            f"terminar ou peça ao dev para encerrar (processos: {', '.join(pids[:5])})."
        )


def pre_bash(entrada):
    comando = (entrada.get("tool_input") or {}).get("command", "")
    if not comando:
        return
    raiz, _ = raiz_do_projeto(entrada)
    config = ler_config(raiz)
    for parte in partes(limpar_comando(comando)):
        checar_git(parte, raiz, config)
        checar_producao(parte, raiz, config)
        checar_testes_simultaneos(parte, config)


# ---------- post-bash ----------

def post_bash(entrada):
    comando = (entrada.get("tool_input") or {}).get("command", "")
    if not re.search(r"\bgit\b[^\n]*\bcommit\b", limpar_comando(comando)):
        return
    raiz, _ = raiz_do_projeto(entrada)
    dados = sh(["git", "log", "-1", "--format=%ct%n%H%n%B"], raiz).split("\n")
    if len(dados) < 3 or time.time() - int(dados[0] or 0) > 120:
        return  # o commit não aconteceu agora: nada a conferir
    sha, mensagem = dados[1][:7], "\n".join(dados[2:]).strip()
    config = ler_config(raiz)
    problemas, avisos = [], []

    if any(re.search(p, mensagem, re.IGNORECASE) for p in ASSINATURAS_CLAUDE):
        problemas.append(
            "a mensagem tem assinatura do Claude (Co-Authored-By, noreply@anthropic.com ou "
            "\"Generated with Claude Code\"). Nada sai assinado pelo Claude"
        )

    regra = config.get("commit", {})
    tipos = regra.get("tipos", ["feat", "fix", "chore", "docs"])
    com_id = regra.get("idObrigatorioEm", ["feat"])
    padrao_id = regra.get("padraoId", r"[A-Z]{2,5}-\d{1,4}")
    titulo = mensagem.split("\n", 1)[0]
    m = re.match(r"^(\w+)(\([^)]*\))?: (.+)$", titulo)
    if not m or m.group(1) not in tipos:
        problemas.append(
            f"título fora do padrão: `{titulo}`. Esperado `tipo: <ID> o que mudou`, com tipo em "
            f"{', '.join(tipos)}"
        )
    elif m.group(1) in com_id and not re.match(padrao_id + r"\b", m.group(3)):
        problemas.append(f"título de `{m.group(1)}` sem o ID da tarefa logo depois dos dois pontos: `{titulo}`")

    doc = config.get("documentacao")
    if doc and doc.get("pasta"):
        arquivos = sh(["git", "show", "--name-only", "--format=", "HEAD"], raiz).split("\n")
        mexeu_codigo = any(a.startswith(tuple(doc.get("codigo", []))) for a in arquivos if a)
        mexeu_doc = any(a.startswith(doc["pasta"]) for a in arquivos if a)
        if mexeu_codigo and not mexeu_doc:
            avisos.append(
                f"o commit mexe em código de módulo e não toca em `{doc['pasta']}`. Se a tarefa "
                "mudou comportamento, o documento da funcionalidade vai no mesmo commit (skill "
                "documentar). Se não mudou, pode seguir"
            )

    if problemas or avisos:
        texto = [f"[harness] Commit {sha}:"]
        if problemas:
            texto += [f"- Corrigir: {p}." for p in problemas]
            texto.append("Corrija com `git commit --amend` antes de qualquer push.")
        texto += [f"- Aviso (não bloqueia): {a}." for a in avisos]
        print("\n".join(texto), file=sys.stderr)
        sys.exit(2)


def main():
    try:
        entrada = json.load(sys.stdin)
    except ValueError:
        return
    acao = sys.argv[1] if len(sys.argv) > 1 else ""
    if acao == "pre-bash":
        pre_bash(entrada)
    elif acao == "post-bash":
        post_bash(entrada)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as erro:  # um defeito do hook nunca trava o dev
        print(f"[harness] hook com erro, ignorado: {erro}", file=sys.stderr)
        sys.exit(0)
