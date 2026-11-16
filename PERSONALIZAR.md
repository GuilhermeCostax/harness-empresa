# Configurar o harness para uma empresa

Este repositório é a **base global**: o processo de desenvolvimento como plugin do Claude Code,
pronto para ser copiado. Cada empresa faz a sua cópia, ajusta o que for dela e instala nos seus
projetos.

```
harness-empresa (base global, este repositório)
  └── cópia da empresa A  →  projetos da empresa A
  └── cópia da empresa B  →  projetos da empresa B
```

Melhoria que serve para todas as empresas entra aqui, por PR. Regra de uma empresa só fica na
cópia dela. Regra de um sistema só fica no `CLAUDE.md` daquele sistema.

## 1. Copiar a base

No GitHub, abrir este repositório e usar **Use this template → Create a new repository**, na
conta ou organização da empresa, como **privado**. Ou pela linha de comando:

```
gh repo create <org-da-empresa>/harness --private --template GuilhermeCostax/harness-empresa --clone
```

## 2. Dar nome e dono

| Arquivo | O que mudar |
| --- | --- |
| `.claude-plugin/plugin.json` | `name` (vira o prefixo das skills: `/<name>:tarefa`), `description`, `author` |
| `.claude-plugin/marketplace.json` | `name` do marketplace, `owner`, e o `name` do plugin igual ao do `plugin.json` |
| `INSTALAR.md` | Trocar `GuilhermeCostax/harness-empresa` pelo repositório da cópia, e `harness@harness-empresa` por `<plugin>@<marketplace>` |
| `modelos/CLAUDE-projeto.md` | O nome do plugin e o link do repositório no aviso do topo |

Conferir depois:

```
claude plugin validate .
```

## 3. Ajustar o processo da empresa

Ler cada arquivo e mudar o que a empresa faz diferente. O que já serve fica como está.

| Arquivo | O que costuma mudar |
| --- | --- |
| `regras/gerais.md` | Idioma e padrão de commit, fluxo de branch (PR ou direto), como tratar regra de negócio e reuniões, logins de teste. Limite de 10 mil caracteres: o hook corta o resto |
| `skills/tarefa/SKILL.md` | As etapas da tarefa. Empresa com outro processo (sem protótipo, com QA separado, com aprovação do cliente) muda aqui |
| `skills/validar/SKILL.md` | O que a IA valida sozinha e o formato do passo a passo para o dev |
| `skills/push/SKILL.md` | Revisão de PR, quem faz o merge, ambientes de deploy |
| `skills/status/SKILL.md` | Onde fica o plano de tarefas (Claude Docs, Jira, GitHub Projects) e o formato padrão de status |
| `skills/documentar/` | O modelo de documento de funcionalidade (`modelo.md`) e as regras de escrita |
| `agents/*.md` | Os revisores: o que cada um confere, o formato do relatório e o modelo (`model:`) |
| `scripts/harness_hooks.py` | As proteções: o que bloquear antes de um comando e o que conferir depois de um commit. O que varia por projeto fica no `.claude/harness.json` do projeto, não aqui |
| `modelos/harness.json` | Os valores de partida que um projeto novo copia |

Mudou o processo, testar numa sessão antes de subir:

```
claude --plugin-dir /caminho/da/copia
```

## 4. Instalar nos devs e nos projetos

Seguir o `INSTALAR.md` da cópia: instalar o plugin em cada máquina e ligar em cada projeto.

## 5. Receber melhorias da base

A cópia não acompanha a base sozinha. Para trazer uma melhoria:

```
git remote add base https://github.com/GuilhermeCostax/harness-empresa.git
git fetch base
git log --oneline HEAD..base/main
```

Trazer só os commits que servem (`git cherry-pick <commit>`), conferindo conflito com o que a
empresa personalizou.
