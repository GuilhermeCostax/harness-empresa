<!--
  Descreva a FUNCIONALIDADE INTEIRA, como ela é hoje — não a alteração da task.
  Presente, estado atual ("aceita e-mail ou CPF"), nunca "passa a", "agora", "antes era".
  O que uma task mudou vai só no Histórico de decisões, no fim.
  Sem data, chamado ou ocorrência pontual no corpo (isso vai no card).
-->
# Nome da funcionalidade

> Uma ou duas frases: o que é e para quem. Ex.: "Permite ao administrador duplicar um modelo
> de documento, com todas as variáveis, para criar uma variação sem cadastrar do zero."

## Como funciona

Fluxo do ponto de vista de quem usa (administrador, funcionário, responsável da empresa,
associado, sistema). Lista numerada quando houver passos.

1. ...
2. ...

## Regras de negócio

Cada regra com o **porquê**. É a seção mais importante.

- **Regra.** Motivo.
- ...

## Configuração

Onde se liga/ajusta (tela, aba, campo, permissão, variável de ambiente) e o efeito de cada
opção. Remover a seção se não houver.

| Onde | Opção | Efeito |
| --- | --- | --- |
| | | |

## Impactos no sistema

O que esta funcionalidade afeta ou de que depende. Ao mudar algo aqui, conferir estes pontos.

| Parte do sistema | Relação |
| --- | --- |
| | |

## Onde está no código

| O quê | Onde |
| --- | --- |
| Backend | `backend/controllers/...` |
| Frontend | `frontend/src/pages/...` |
| Testes | `..._test.go` |

## Pendências e limitações

O que ainda não foi validado, o que se sabe que não cobre, dívidas conhecidas.

## Histórico de decisões

Única seção que fala de mudanças: uma linha por decisão, com a task e o porquê.

| Data | Task | Decisão |
| --- | --- | --- |
| AAAA-MM-DD | ACE-03 | ... |
