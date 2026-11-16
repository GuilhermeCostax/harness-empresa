# harness-empresa

Plugin do Claude Code com o processo de desenvolvimento da empresa. Cada projeto instala o
plugin e escreve só o próprio `CLAUDE.md`, com a seção **Dados do projeto (harness)**.

## O que tem

| Parte | Onde | O que faz |
| --- | --- | --- |
| Regras gerais | `regras/gerais.md` | Entram em toda sessão pelo hook `SessionStart` |
| `/harness:tarefa <ID>` | `skills/tarefa/` | Conduz as 7 etapas de uma tarefa |
| `/harness:validar <ID>` | `skills/validar/` | Etapa 5: a IA valida o que é comando, o dev testa as telas |
| `/harness:push <ID>` | `skills/push/` | Etapa 7: integra sem quebrar o trabalho dos outros e sobe |
| `/harness:status <ID> <status>` | `skills/status/` | Status, Quem, módulo e gráfico no plano |
| `/harness:documentar` | `skills/documentar/` | Documento da funcionalidade, pelo modelo |
| Modelo de projeto | `modelos/CLAUDE-projeto.md` | Esqueleto do `CLAUDE.md` de um projeto novo |
| Gerador do AGENTS.md | `scripts/gerar-agents.sh` | Junta projeto + regras + skills para o Codex |

O dev não precisa chamar as skills pelo nome: "faz a EMP-14" já aciona a `tarefa`.

## Instalar (por enquanto, local)

```
claude plugin marketplace add /caminho/para/harness-empresa
claude plugin install harness@harness-empresa
```

Para testar só numa sessão, sem instalar: `claude --plugin-dir /caminho/para/harness-empresa`.

Conferir o plugin depois de mudar: `claude plugin validate /caminho/para/harness-empresa`.

## Mudar uma regra

1. Regra que vale para todo projeto: editar aqui, por PR revisado por outro dev.
2. Regra de um projeto só: editar o `CLAUDE.md` daquele projeto.
3. Depois de qualquer um dos dois, gerar de novo o `AGENTS.md` do projeto:

```
scripts/gerar-agents.sh /caminho/do/projeto
```
