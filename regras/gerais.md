# Harness da empresa — regras gerais

> Parte destas regras é garantida por hooks: push forçado, `git reset --hard`, comando que mexe
> em dados com o banco de produção configurado, duas execuções de testes ao mesmo tempo e
> commit fora do padrão são barrados ou devolvidos com o motivo. Bloqueio do harness não se
> contorna: explicar ao dev e deixar a decisão com ele.

Estas regras valem em todo projeto da empresa. O que é de cada projeto (stack, comandos, links,
armadilhas) está no `CLAUDE.md` dele, na seção **Dados do projeto (harness)**. Se um projeto não
tiver essa seção, avisar o dev antes de começar uma tarefa.

Em caso de conflito, o `CLAUDE.md` do projeto vale sobre estas regras: ele conhece o caso
concreto.

## Como o trabalho anda

- Toda tarefa começa pelo **ID do plano** do projeto (ex.: "faz a `ACE-03`"). Tarefa pedida sem
  ID, ou que não está no plano: perguntar o ID ao dev antes de começar.
- Com o ID, seguir a skill **tarefa**, que conduz as 7 etapas em ordem. Não pular etapa.
- Etapa 5 é a skill **validar**, a 7 é a skill **push**, e toda mudança de status no plano segue
  a skill **status**. Documento de funcionalidade segue a skill **documentar**.

## Ao fechar uma tarefa

Cada tarefa começa do zero, lendo o plano e a documentação. O histórico da tarefa anterior só
atrapalha. Com a tarefa em **Feito** (ou parada para o dia):

1. Salvar no **arquivo de contexto** do projeto (ver *Dados do projeto*) só o que a próxima
   sessão precisa: estado das tarefas, pendências com outros devs, dúvidas em aberto. O que é regra
   de negócio já está no documento da funcionalidade; não repetir.
2. Sugerir a próxima tarefa: a primeira livre do módulo do dev no plano (sem *Quem*, com as
   dependências em **Feito**), seguindo a ordem que o dev combinou, se houver uma no arquivo de
   contexto. Dizer quais estão esperando outros módulos e por quê.
3. Dizer ao dev, em uma linha, que pode rodar `/clear` antes da próxima tarefa. Só o dev roda; a
   IA não consegue limpar o contexto sozinha.

`/compact` é para o meio de uma tarefa longa: resume a conversa e continua nela. Entre tarefas, o
certo é `/clear`.

## Regra de negócio: nunca adivinhar

Quando o plano não basta, consultar nesta ordem, usando o que o projeto lista em *Dados do
projeto*:

1. O doc de regras de negócio do projeto. Ler só a aba e o trecho em questão.
2. As transcrições das reuniões.
3. Ainda sem resposta: perguntar ao dev antes de implementar.

Ao ler transcrição de reunião:

- Buscar pelo assunto (`grep -n`) e ler a seção inteira, não o arquivo todo.
- Vale a **conclusão** do trecho, não a primeira ideia. O time discute antes de decidir.
- Trecho marcado `[?]` ficou pouco audível: não vira regra sem confirmar com o dev.
- Reunião × protótipo: vale a reunião. Reunião × plano: o plano é mais recente, mas não escolher
  sozinho, perguntar ao dev.
- A regra confirmada vai para o documento da funcionalidade, com o porquê.

## Documentação de funcionalidades

O projeto guarda a documentação do que **está implementado** (ex.: `funcionalidades/`).
Plano, protótipo e reuniões são o **alvo**; a documentação é o estado atual.

- **O código é a fonte da verdade.** Documento que contradiz o código é corrigido pelo código, e
  a divergência é avisada ao dev. Nunca o contrário sem o dev decidir.
- **Antes de mexer** numa funcionalidade, ler o documento dela.
- **Toda tarefa que muda comportamento atualiza o documento no mesmo commit.**
- O documento é da funcionalidade, não da tarefa: presente, estado atual. A mudança em si vai só
  no *Histórico de decisões*. Detalhes na skill **documentar**.
- **Pendência que espera outra tarefa cita o ID dela.** É por esse ID que a tarefa, ao começar,
  acha o que precisa resolver.

## Testes

- Toda tarefa entrega o teste da funcionalidade e roda **só os testes da tarefa**, não a suíte
  inteira.
- Correção de defeito: o teste precisa **falhar sem a correção** e passar com ela. Rodar uma vez
  antes de corrigir para provar.
- **`ok` não basta.** Rodar em modo detalhado e conferir que nenhum teste da tarefa foi pulado.
  Teste pulado não é teste que passou.
- Teste nunca usa endereço de banco fixo nem credencial própria: usa o auxiliar de testes do
  projeto, para rodar igual na máquina de qualquer dev.
- Falha que só aparece com outra execução rodando junto não é defeito do código: rodar sozinho
  antes de acusar a alteração.

## Git e commits

- **Fluxo padrão: uma branch por tarefa e PR para a branch principal.** Projeto que sobe direto
  na principal diz isso no `CLAUDE.md`, e aí vale o projeto.
- **Só commitar, dar push ou abrir PR quando o dev pedir.** O normal é deixar no working tree
  para revisão. Merge é do dev ou do revisor, nunca da IA por conta própria.
- **Nunca `git push --force` na branch principal, nem `git reset --hard`** para resolver
  conflito: apaga o trabalho de outro dev. Na branch da própria tarefa, depois de um rebase, só
  `--force-with-lease`.
- Conflito: resolver mantendo **as duas** alterações funcionando. Sem entender a intenção do outro
  lado, parar e perguntar ao dev.
- **Nada assinado pelo Claude.** Commit, PR, comentário de PR ou issue sai em nome do dev, sem
  `Co-Authored-By: Claude`, sem "Generated with Claude Code" e sem qualquer menção à IA. O
  `.claude/settings.json` do projeto desliga a assinatura automática (`attribution`); a regra
  vale mesmo se a configuração faltar.
- Commits pequenos, uma tarefa por commit, com a documentação junto.
- Mensagem em Conventional Commits, em **pt-BR**:
  - Título: `tipo: <ID> o que mudou`, curto, no presente. Tipos: `feat`, `fix`, `chore`, `docs`.
    O ID é obrigatório em `feat`; num `fix` de defeito fora do plano pode faltar, nunca inventar um.
  - Corpo: um parágrafo com o **defeito ou a motivação** (o que acontecia e por quê), depois
    bullets do que mudou, incluindo a linha da documentação atualizada.

Exemplo:

```
fix: ACE-07 funcionário desativado continuava navegando até o token expirar

Desativar o funcionário só bloqueava o próximo login. As sessões abertas
seguiam válidas porque o middleware conferia o JWT, mas não a conta.

- AuthMiddleware confere a conta ativa a cada requisição
- desativar derruba todas as sessões (motivo funcionario_desativado)
- funcionalidades/acesso/login-e-sessoes: regra e histórico atualizados
```

## Código

- O comentário explica o **porquê** e o problema que o código resolve, não o que a linha faz.
  Regra que não é óbvia leva o motivo e o caso real que a motivou, para ninguém "simplificar" sem
  saber.
- Nunca reformatar arquivo que a tarefa não tocou.

## Logins e dados de teste

- O projeto tem um **acesso padrão** de teste (ver *Dados do projeto*). Se não existir na máquina,
  criar antes do primeiro passo a passo.
- Cenário específico da tarefa usa um **acesso temporário** com o ID da tarefa no nome. Com o
  "está tudo correto" do dev, a IA apaga os acessos temporários da tarefa.
- No chat, citar o login pela linha do arquivo de logins, **sem repetir a senha**.
- Usuário e dado de teste só no banco de desenvolvimento, nunca num ambiente que aponte para
  produção.
