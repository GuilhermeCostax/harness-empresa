---
name: documentar
description: Cria ou atualiza o documento de uma funcionalidade na pasta de documentação do projeto (por exemplo funcionalidades/), seguindo o modelo da empresa. Use em toda tarefa que muda comportamento, antes de editar qualquer arquivo dessa pasta, ou quando o dev pedir para documentar uma funcionalidade.
argument-hint: <módulo/funcionalidade> [ID da tarefa]
---

# Documentar a funcionalidade — $ARGUMENTS

A pasta de documentação vem de **Dados do projeto (harness)** no `CLAUDE.md`. Se ela tiver um
`README.md` com regras de escrita, ler antes de criar ou editar qualquer arquivo, inclusive uma
linha de tabela.

## O documento é da funcionalidade, não da tarefa

- Descreve a **funcionalidade inteira, como ela é hoje**: o que faz, todas as regras de negócio e
  o que ela afeta.
- Presente, estado atual: "o login aceita e-mail ou CPF", nunca "passa a aceitar", "agora",
  "antes era", "virou".
- Ao atualizar, **reescrever** a parte afetada; não acrescentar um parágrafo sobre a mudança.
- A mudança em si (o que, quando, por quê, ID da tarefa) vai **só** no *Histórico de decisões*.
- Nada de data, número de chamado, nome de quem atendeu ou ocorrência pontual no corpo. O corpo
  precisa continuar verdade amanhã.

## Criar

1. Usar o modelo do projeto (ex.: `funcionalidades/_modelo/README.md`). Se o projeto não
   tiver um, usar o [modelo do plugin](modelo.md).
2. Pasta `<módulo>/<funcionalidade>/`, nome em minúsculas com hífen, pelo nome que o time usa.
3. Ler o código da funcionalidade inteira, **tela e backend**, não só o que a tarefa tocou.
4. O que não deu para conferir no código vai em *Pendências*, dito com todas as letras.
5. Adicionar a linha no índice da pasta, na ordem do índice.

## Atualizar

| A tarefa mudou | Seção |
| --- | --- |
| Regra de negócio | *Regras de negócio*, com o porquê |
| Tela, campo, permissão ou variável de ambiente | *Configuração* |
| Outra parte do sistema | *Impactos*, **nos dois documentos** |
| Qualquer coisa | Uma linha no *Histórico de decisões* com data, ID e porquê |

## Como escrever

- Para **gente**: o porquê, não só o quê. "O funcionário desativado cai na hora porque a sessão é
  conferida a cada requisição" vale mais que "middleware checa is_active".
- Começar pela visão de quem usa; o código vem em *Onde está no código*.
- Citar arquivos e funções pelo nome, sem copiar código.
- Frases curtas, tabelas para comparar, listas numeradas para fluxo.
- **Pendência que espera outra tarefa cita o ID dela** ("entra com a EMP-06"). Quando a tarefa
  resolve a pendência, ela sai do documento e a decisão vai para o *Histórico de decisões*.

## Código é a fonte da verdade

Documento e código divergem: o documento é corrigido para o que o código faz, e a divergência é
avisada ao dev, que decide se o código é que está errado. Nunca mudar o código só para bater com
um documento sem o dev decidir.
