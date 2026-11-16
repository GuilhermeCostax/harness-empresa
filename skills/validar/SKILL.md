---
name: validar
description: Etapa 5 do processo da empresa. A IA valida sozinha tudo o que se testa por comando (build, testes da tarefa, migration, rotas da API, dados no banco de dev) e entrega ao dev só o passo a passo do que se testa nas telas. Use ao terminar de desenvolver e testar uma tarefa, antes de pedir a revisão do dev.
argument-hint: <ID da tarefa>
---

# Validar a tarefa $ARGUMENTS

O dev não roda teste no terminal nem cria cadastro para testar: isso é trabalho da IA. O dev só
usa o sistema. Comandos, banco de dev e logins vêm de **Dados do projeto (harness)** no
`CLAUDE.md`.

## 1. O que a IA faz sozinha

Fazer e relatar o resultado de cada item:

- build e checagem estática do projeto, limpos;
- os testes da tarefa passando, em modo detalhado, **nenhum pulado**;
- migration rodada no banco de dev e a tabela ou coluna conferida no banco;
- rotas da API exercitadas com o login certo, incluindo os casos que devem ser **recusados**: sem
  login (401), sem permissão (403), dado inválido (422), inexistente (404). Se a API do dev estiver
  rodando com código antigo, subir uma temporária em outra porta, sem derrubar a dele;
- dado que o teste precisa e não existe no banco de dev é **criado pela IA**, de preferência pela
  própria API;
- itens extras de *Pronto* que o projeto lista em *Dados do projeto*.

## 1b. Revisão por quem não escreveu o código

Antes de entregar ao dev, chamar **ao mesmo tempo** dois sub-agentes do harness, passando o ID
da tarefa e os arquivos mudados:

- **verificador** (`harness:verificador`): confere o *Pronto* geral e os itens extras do
  projeto, com a prova de cada um. Passar para ele o resultado do testador da etapa 4;
- **documentador** (`harness:documentador`): compara o documento da funcionalidade com o código.

Corrigir o que eles apontarem e chamar de novo até não sobrar nada, ou até sobrar só o que
depende de decisão do dev. O que sobrar vai no relatório da parte 1, com todas as letras.
Divergência entre documento e código nunca se resolve mudando o código sem o dev decidir.

A IA não abre navegador, não tira print e não pede para conferir pixel, a menos que o projeto
diga o contrário.

## 2. O passo a passo para o dev

Só o que se testa usando o sistema:

1. **Preparar** — o que precisa estar rodando e **com qual login entrar** (pela linha do arquivo
   de logins, sem repetir a senha).
2. **Testar** — passos numerados na tela: onde clicar, o que preencher e **o que deve
   acontecer** em cada passo. Um bloco por regra de negócio, incluindo o que a tela deve
   **recusar** (campo inválido, sem permissão, duplicado).
3. **Conferir a estética** — o que comparar com a mesma tela na referência visual do projeto.
4. **Conferir que nada quebrou** — telas e funcionalidades vizinhas, as de *Impactos* no
   documento da funcionalidade.

Tarefa só de backend: o passo a passo cobre o que aparece em alguma tela (ex.: a permissão nova
na tela de cargos), e o resto fica no relatório da parte 1.

## 3. Status

Entregue o passo a passo, a tarefa vai para **Em revisão** (skill **status**). O commit só
acontece depois que o dev valida e diz que está tudo correto.
