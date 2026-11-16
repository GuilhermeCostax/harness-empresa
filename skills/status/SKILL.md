---
name: status
description: Atualiza o status de uma tarefa no plano do projeto (A fazer, Fazendo, Em revisão, Feito, Travada), o Quem, o status do módulo e o gráfico de progresso. Use sempre que uma etapa da tarefa mudar o status, ou quando o dev pedir para atualizar o plano.
argument-hint: <ID da tarefa> <novo status>
---

# Status no plano — $ARGUMENTS

O link do plano vem de **Dados do projeto (harness)** no `CLAUDE.md`. Plano no Claude Docs: ler e
editar **só com as ferramentas do conector Claude Docs**, nunca por web fetch. Ferramenta sem
acesso ao plano: avisar o dev para ele mudar à mão.

## Regras de edição

- **Não reescrever o plano.** Só mudar *Status* e *Quem* das tarefas e o *Status* do módulo.
  Regra nova, tarefa nova ou mudança de escopo: propor ao dev, não editar por conta própria.
- Ler só a seção do módulo e a linha da tarefa (busca pelo ID), nunca o documento inteiro.
- Vários devs editam ao mesmo tempo: ler a linha logo antes de mudar. Se ela mudou desde a
  leitura, manter o que o outro escreveu e avisar o dev.

## Formato do plano é do projeto

Cada projeto organiza o plano do seu jeito. Os nomes dos status, as colunas (*Quem*, *Depende*…),
o status do módulo e o gráfico vêm do `CLAUDE.md` do projeto. Valem os nomes dele, mesmo que
sejam outros. O que o projeto não definir segue o padrão abaixo. Plano sem algum desses itens
(sem coluna de módulo, sem gráfico): pular o item, sem criar nada no plano.

## Status da tarefa (padrão)

Opções: **A fazer**, **Fazendo**, **Em revisão**, **Feito**, **Travada**.

| Quando | Status | Também |
| --- | --- | --- |
| Etapa 1, começou a tarefa | **Fazendo** | Usuário do GitHub do dev em *Quem* |
| Etapa 5, passo a passo entregue | **Em revisão** | |
| Etapa 6, o dev pediu alteração | **Fazendo** | |
| Etapa 7, PR aberto | continua **Em revisão** | |
| Etapa 7, merge do PR (ou push, se o projeto sobe direto na principal) | **Feito** | Nunca antes |
| Bloqueada (dependência, dúvida sem resposta) | **Travada** | Comentário na linha com o motivo |

**Quem** = o usuário do GitHub do dev, lido com `gh api user --jq .login`. Sem o `gh` logado,
perguntar ao dev. Nunca o nome do `git config`, que muda de máquina para máquina.

## Status do módulo (padrão)

Opções: **A fazer**, **Fazendo**, **Concluído**.

- Primeira tarefa do módulo em **Fazendo**: o módulo vai para **Fazendo**.
- Tarefa foi para **Feito**: ler a tabela de tarefas do módulo inteira. Todas **Feito**: o módulo
  vai para **Concluído**. Falta alguma: continua **Fazendo**.

## Gráfico de progresso

Se o plano tiver um gráfico de progresso por módulo, os números ficam gravados no próprio
gráfico, não lidos das tabelas. **Toda mudança de status atualiza a linha do módulo no gráfico na
mesma hora**, senão ele mostra um progresso falso.

1. Ler o widget do gráfico (`read` com `engine: "widget"` no nó do embed da seção de progresso).
2. Trocar só os números da linha do módulo (`feito`, `em_revisao`, `fazendo`, `travada`,
   `a_fazer`, e `total` se o plano ganhou tarefa) com `draft-edit`, depois `publish`. Não
   redesenhar o gráfico.
3. Conferir que `feito + em_revisao + fazendo + travada + a_fazer = total` na linha alterada.
