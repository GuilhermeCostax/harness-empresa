---
name: tarefa
description: Conduz uma tarefa do plano do projeto pelas 7 etapas do processo da empresa (ler, protótipo, desenvolver, testar, validar, retorno do dev, push). Use quando o dev pedir para fazer, começar ou continuar uma tarefa pelo ID do plano, como "faz a EMP-14" ou "continua a ACE-03".
argument-hint: <ID da tarefa, ex. EMP-14>
---

# Tarefa $ARGUMENTS

Conduzir a tarefa pelas 7 etapas, em ordem, sem pular nenhuma. O status no plano acompanha cada
etapa (skill **status**), sem o dev precisar pedir.

Os caminhos, links e comandos citados como "do projeto" estão na seção **Dados do projeto
(harness)** do `CLAUDE.md`. Sem essa seção, parar e avisar o dev.

Sem ID na chamada, ou ID que não está no plano: perguntar ao dev qual é o ID antes de começar.

## Etapa 1 — Ler a tarefa

1. No plano do projeto, ler só o necessário: a linha da tarefa, a seção do módulo e as tarefas
   da coluna *Depende*. Nunca o plano inteiro.
2. Conferir se a tarefa não está com outro dev e se as dependências estão **Feito**. Dependência
   não pronta: status **Travada** com o motivo, e avisar o dev.
3. Estando livre: status **Fazendo** e o usuário do GitHub do dev em *Quem* (skill **status**).
4. Fluxo por PR (o padrão, ver skill **push**): criar a branch da tarefa a partir da principal
   atualizada, `git fetch origin && git switch -c <tipo>/<ID>-<resumo> origin/<principal>`
   (ex.: `feat/EMP-14-contratos`). Projeto que sobe direto na principal: não criar branch.
5. Ler o documento da funcionalidade, se ela já existir.
6. **Buscar as pendências que a tarefa resolve:** `grep -rn "<ID>"` na pasta de documentação do
   projeto. Toda pendência que espera esta tarefa entra no escopo: resolver junto (e tirar a
   pendência do documento) ou, se não der, avisar o dev.
7. Dúvida de regra de negócio: seguir a ordem das regras gerais (doc de regras, reuniões, dev).
   Não adivinhar.

## Etapa 2 — Referência visual

Se o projeto tiver protótipo ou referência visual (ver *Dados do projeto*), achar a tela dele e
seguir **fielmente a estética**: layout, textos, ordem dos campos, cores, espaçamentos, estados
(vazio, carregando, erro). A implementação é com a stack do projeto, nunca copiando o HTML do
protótipo. Onde uma reunião mudou o protótipo, vale a reunião.

Tarefa sem tela: pular para a etapa 3 e dizer isso ao dev.

## Etapa 3 — Desenvolver

1. Backend e frontend, dentro das pastas que o projeto define para a tarefa.
2. Atualizar ou criar o documento da funcionalidade (skill **documentar**).
3. Build e checagem estática do projeto limpos ao final.

## Etapa 4 — Testar

Escrever o teste da funcionalidade. Correção de defeito: provar antes que o teste falha sem a
correção.

Rodar pelo sub-agente **testador** do harness (`harness:testador`), passando o ID e os testes da
tarefa. Ele roda só esses testes, em modo detalhado, e conta pulado como problema. Falha ou pulo:
corrigir e chamar o testador de novo.

## Etapa 5 — Validar

Seguir a skill **validar**: a IA valida tudo o que é comando e entrega ao dev o passo a passo das
telas. A tarefa vai para **Em revisão**.

## Etapa 6 — Retorno do dev

- O dev pediu alteração: status **Fazendo** e voltar à etapa 3.
- O dev disse que está tudo correto: apagar os acessos temporários da tarefa e seguir para a
  etapa 7.

## Etapa 7 — Push

Só depois do "está tudo correto" **e** do pedido do dev para subir. Seguir a skill **push**: por
PR (padrão), a tarefa vai para **Feito** com o merge; direto na principal, com o push.
