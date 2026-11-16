---
name: comparar-tela
description: Entrega de tarefa com tela para o dev que ligou o teste no navegador. Depois da validação por comando, a IA testa as telas no navegador sem perguntar, tira os prints do protótipo e do sistema, monta a página de comparação lado a lado e abre no navegador do dev. Use na etapa 5 de toda tarefa com tela, junto com a skill validar do harness.
argument-hint: <ID da tarefa>
---

# Comparar tela — $ARGUMENTS

Este dev ligou o plugin `harness-navegador`: ele quer validar a tarefa **olhando**, sem refazer o
passo a passo à mão. Para ele, a regra "a IA não abre navegador" da skill **validar** não vale.
O resto da validar continua igual (validação por comando, passo a passo no relatório, revisores).

A ferramenta, as URLs e o login vêm de **Dados do projeto (harness)** no `CLAUDE.md` (linha
*Teste no navegador*) e do `LEIA-ME.md` da ferramenta. Projeto sem essa linha: avisar o dev e
seguir só a validar.

Tarefa sem tela: não há o que comparar; dizer isso e parar aqui.

## 1. Testar nas telas, sem perguntar

Depois da parte 1 da validar (tudo o que é comando passou):

1. Abrir o sistema no navegador embutido do app (ferramentas `mcp__Claude_Browser__*`; sem elas,
   pular para o passo 2 e dizer ao dev que o teste clicando ficou de fora).
2. Entrar com o acesso padrão de teste do projeto.
3. Seguir o passo a passo que a validar escreveu: cada regra, incluindo o que a tela deve
   **recusar**. Anotar o que aconteceu em cada passo.

## 2. Prints e página de comparação

1. Escrever `capturas-teste/<ID>/roteiro.mjs` com as telas que a tarefa mexeu: o mesmo estado no
   protótipo e no sistema. Arquivos que o sistema gera (PDF, planilha) a ferramenta baixa sozinha
   para `arquivos-teste/<ID>/` — conferir o conteúdo (o Read lê PDF) em vez de pedir ao dev.
2. Rodar a captura e conferir os prints antes de seguir (tela de login, erro ou carregando no
   print = refazer).
3. Escrever `capturas-teste/<ID>/comparacao.mjs`: para cada bloco, o que conferir e as diferenças
   **esperadas** (o que a reunião mudou em relação ao protótipo, o que ficou para outra tarefa).
4. Gerar a página e **abrir no navegador do dev** (`open capturas-teste/<ID>/comparacao.html`).
   Não mandar só a pasta de imagens; o painel lateral do app é estreito demais para comparar.

Protótipo e sistema saem como abrem na máquina do dev (tema dele). Não forçar tema.

## 3. Uma mensagem só

Entregar junto, na mesma mensagem: o relatório da validar, o resultado do teste nas telas (passo
a passo, com o que deu certo e o que não) e o caminho da página já aberta. O dev responde "está
tudo correto" ou o ajuste.

Tarefas pequenas vizinhas podem sair numa página só, mas com um commit por tarefa.

## 4. Limpeza

Com a tarefa em **Feito**: apagar `capturas-teste/<ID>/` e `arquivos-teste/<ID>/`. Print do
protótipo que uma tarefa futura vai usar vai para `capturas-teste/<ID-futura>/referencia-prototipo/`
com um `LEIA-ME.md` dizendo o porquê, e o dev é avisado.

Essas pastas nunca vão para o git.
