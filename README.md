# harness-empresa

Base global do processo de desenvolvimento como **plugin do Claude Code**. Cada empresa copia esta
base, ajusta o que for dela e instala nos seus projetos. Cada projeto escreve só o próprio
`CLAUDE.md`, com a seção **Dados do projeto (harness)**.

| Quero… | Ler |
| --- | --- |
| Configurar o harness para uma empresa | [PERSONALIZAR.md](PERSONALIZAR.md) |
| Instalar numa máquina ou ligar num projeto | [INSTALAR.md](INSTALAR.md) |

## O que tem

| Parte | Onde | O que faz |
| --- | --- | --- |
| Regras gerais | `regras/gerais.md` | Entram em toda sessão pelo hook `SessionStart` |
| `/harness:tarefa <ID>` | `skills/tarefa/` | Conduz as 7 etapas de uma tarefa, com branch por tarefa |
| `/harness:validar <ID>` | `skills/validar/` | Etapa 5: a IA valida o que é comando, o dev testa as telas |
| `/harness:push <ID>` | `skills/push/` | Etapa 7: integra sem quebrar o trabalho dos outros e abre o PR |
| `/harness:status <ID> <status>` | `skills/status/` | Status no plano, no formato que o projeto define |
| `/harness:documentar` | `skills/documentar/` | Documento da funcionalidade, pelo modelo |
| Hooks de proteção | `hooks/hooks.json` + `scripts/harness_hooks.py` | Bloqueiam push forçado, `reset --hard`, produção e testes simultâneos; conferem cada commit |
| Modelo de projeto | `modelos/CLAUDE-projeto.md` | Esqueleto do `CLAUDE.md` de um sistema novo |
| Configuração dos hooks | `modelos/harness.json` | Vai para `.claude/harness.json` de cada projeto |

O dev não precisa chamar as skills pelo nome: "faz a EMP-14" já aciona a `tarefa`.

## Padrões que a base já traz

- Uma branch por tarefa e PR para a branch principal. O projeto pode optar por subir direto.
- Opus 5.5 com esforço médio, definido no `.claude/settings.json` de cada projeto (um plugin não
  consegue fixar o modelo).
- Ao fechar uma tarefa: salvar o que importa no arquivo de contexto e limpar a conversa com
  `/clear`.
- Nada sai assinado pelo Claude: commits e PRs em nome do dev (`attribution` vazio no
  `.claude/settings.json` do projeto, e a regra escrita nas regras gerais).
- Só Claude Code. Não há versão para o Codex.

## Mudar uma regra

| A regra vale para… | Onde mudar |
| --- | --- |
| Todas as empresas | Aqui, por PR revisado por outro dev |
| Uma empresa | Na cópia daquela empresa |
| Um sistema | No `CLAUDE.md` daquele sistema |
