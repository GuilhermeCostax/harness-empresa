# Instalar o harness num ambiente novo

Passo a passo para um dev começar a usar o harness numa máquina nova, e para ligar o harness num
projeto novo. Para configurar o harness para outra empresa, ver
[PERSONALIZAR.md](PERSONALIZAR.md) primeiro.

## 1. O que precisa antes

| O quê | Como conferir |
| --- | --- |
| Claude Code instalado e logado na conta do dev | `claude --version` e `/login` dentro do Claude Code |
| Git com acesso ao GitHub (o repositório do plugin é público) | `git ls-remote https://github.com/GuilhermeCostax/harness-empresa` funciona |
| GitHub CLI logado (o harness usa para preencher o *Quem* do plano) | `gh api user --jq .login` mostra o usuário |
| Conector Claude Docs ligado (planos e docs de regras ficam lá) | No Claude Code, o plano do projeto abre pelas ferramentas de Docs |
| Python 3.9 ou mais novo (os hooks de proteção rodam em Python) | `python3 --version`. Sem ele, os hooks não rodam e nada é bloqueado |

## 2. Instalar o plugin na máquina

Uma vez por máquina:

```
claude plugin marketplace add GuilhermeCostax/harness-empresa
claude plugin install harness@harness-empresa
```

Conferir:

```
claude plugin list
```

A lista mostra `harness@harness-empresa`. Dentro do Claude Code, digitar `/harness:` mostra as
skills `tarefa`, `validar`, `push`, `status` e `documentar`, e o comando `/agents` lista os
sub-agentes `verificador`, `documentador`, `testador` e `integrador`.

## 3. Abrir um projeto que já usa o harness

O projeto tem um `.claude/settings.json` com o marketplace e o plugin. Ao abrir o projeto e
confiar na pasta, o Claude Code já sabe de onde vem o plugin. Se ele avisar que o plugin está
ligado no projeto mas não instalado, rodar o passo 2.

Teste rápido: abrir o Claude Code no projeto e pedir "faz a <ID de uma tarefa>". Ele deve começar
pela etapa 1, lendo a linha da tarefa no plano.

## 4. Atualizar o plugin

O `.claude/settings.json` do projeto liga a atualização automática (`"autoUpdate": true` no
marketplace): o Claude Code busca a versão nova ao iniciar. Marketplace do GitHub vem com isso
desligado por padrão, então confira uma vez: `/plugin` → aba **Marketplaces** → `harness-empresa`
→ **Enable auto-update** (se já estiver ligado, não aparece).

Para atualizar na hora, sem esperar:

```
claude plugin marketplace update harness-empresa
claude plugin update harness@harness-empresa
```

Reiniciar o Claude Code depois.

## 4b. Opcional, por dev: teste no navegador

O plugin `harness-navegador` faz a IA testar as telas no navegador e entregar uma página com o
protótipo e o sistema lado a lado. É **por dev**: liga quem quer, só na própria máquina, e o resto
do time não é afetado.

```
claude plugin install harness-navegador@harness-empresa --scope local
```

Rodar dentro da pasta do projeto. O `--scope local` grava a escolha no
`.claude/settings.local.json` do projeto, que é pessoal e fica fora do git (o projeto precisa ter
esse arquivo no `.gitignore`). Para desligar: `claude plugin uninstall harness-navegador@harness-empresa --scope local`.

Precisa de Node, Google Chrome e, para o teste clicando nas telas, do app desktop do Claude
(navegador embutido). O projeto precisa da linha *Teste no navegador* em **Dados do projeto
(harness)**, apontando a ferramenta de captura dele.

## 5. Ligar o harness num projeto novo

1. Copiar `modelos/CLAUDE-projeto.md` para a raiz do projeto como `CLAUDE.md` e preencher a
   seção **Dados do projeto (harness)**, a stack, a organização do código e as armadilhas.
2. Criar `.claude/settings.json` no projeto. Ele liga o plugin, fixa o padrão de modelo (Opus 5.5)
   e de esforço (médio) e tira a assinatura do Claude de commits e PRs (`attribution` vazio).
   Quem precisar de outro modelo na própria máquina muda no `.claude/settings.local.json` ou com
   `/model` e `/effort` na sessão.

   ```json
   {
     "model": "claude-opus-5-5",
     "effortLevel": "medium",
     "attribution": { "commit": "", "pr": "" },
     "extraKnownMarketplaces": {
       "harness-empresa": {
         "source": { "source": "github", "repo": "GuilhermeCostax/harness-empresa" },
         "autoUpdate": true
       }
     },
     "enabledPlugins": {
       "harness@harness-empresa": true
     }
   }
   ```

3. Copiar `modelos/harness.json` para `.claude/harness.json` e ajustar ao projeto (tabela
   abaixo). É o que os hooks de proteção leem.
4. Criar a pasta de documentação de funcionalidades com o modelo
   (`skills/documentar/modelo.md` vira `<pasta>/_modelo/README.md`).
5. Pôr no `.gitignore` o arquivo de logins de teste e o arquivo de contexto que o `CLAUDE.md`
   cita.
6. Commitar `CLAUDE.md`, `.claude/settings.json`, `.claude/harness.json` e o `.gitignore` juntos.

### O `.claude/harness.json`

Cada bloco liga uma proteção. Bloco que falta é proteção desligada, sem erro. O bloqueio de push
forçado e de `git reset --hard` vale sempre, mesmo sem o arquivo.

| Bloco | O que protege | Campos |
| --- | --- | --- |
| `branchPrincipal` | Push forçado na principal | Nome da branch. Sem ele, usa a do `origin` ou `main` |
| `producao` | Comando que mexe em dados rodando contra produção | `arquivoEnv`; `variavelAmbiente` + `valoresProibidos` (ex.: `APP_ENV=production`); `variaveisDeBanco` cujo host precisa estar em `hostsLocais`; `comandos` que contam como "mexe em dados" |
| `testes` | Duas execuções de testes ao mesmo tempo no mesmo banco | `comandos` de teste; `processoEmExecucao`, o padrão de processo (do `pgrep -f`) que indica teste rodando |
| `documentacao` | Commit que mexe no código sem tocar no documento (só avisa) | `pasta` da documentação; `codigo`, as pastas que contam como código de funcionalidade |
| `commit` | Título fora do padrão e assinatura do Claude | `tipos` aceitos; `idObrigatorioEm`, os tipos que exigem ID; `padraoId`, a forma do ID |
| `comandosProibidos` | Comandos que a IA nunca roda no projeto (ex.: apagar ou derrubar o banco) | Lista de `padrao` (expressão regular, sem diferenciar maiúsculas; vale também dentro de aspas, como em `mysql -e "..."`) e `motivo` |

O hook nunca mostra nem guarda valores do `.env`: só confere se o host do banco é local.

## 5a. O que os hooks fazem

| Quando | Hook | Resultado |
| --- | --- | --- |
| Início da sessão | Regras gerais | Entram no contexto |
| Antes de um comando | `git push --force`, `-f`, `+refspec` | Bloqueia; na branch da tarefa, só `--force-with-lease` |
| Antes de um comando | `--force-with-lease` na principal | Bloqueia |
| Antes de um comando | `git reset --hard` | Bloqueia |
| Antes de um comando | Comando de `producao.comandos` com produção no `.env` | Bloqueia |
| Antes de um comando | Teste com outra execução de teste rodando | Bloqueia |
| Antes de um comando | Comando de `comandosProibidos` | Bloqueia, com o motivo |
| Depois de um commit | Título fora do padrão, ID faltando, assinatura do Claude | Devolve ao Claude para corrigir com `--amend` |
| Depois de um commit | Código mudou e documentação não | Avisa, sem exigir nada |

Os hooks só valem para os comandos do Claude. O que o dev roda no próprio terminal não passa por
eles.

## 6. Testar uma mudança no plugin antes de subir

Sem instalar nada, só nesta sessão:

```
claude --plugin-dir /caminho/para/harness-empresa
```

E conferir os arquivos do plugin:

```
claude plugin validate /caminho/para/harness-empresa
```
