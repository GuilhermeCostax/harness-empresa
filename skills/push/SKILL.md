---
name: push
description: Etapa 7 do processo da empresa. Commita a tarefa, confere o que os outros devs subiram, integra sem quebrar o trabalho deles e sobe — por PR (padrão) ou direto na branch principal, se o projeto usar esse fluxo. Use só quando o dev disser que a tarefa está correta e pedir para commitar, subir, abrir o PR ou dar push.
argument-hint: <ID da tarefa>
---

# Subir a tarefa $ARGUMENTS

Só rodar depois de o dev dizer que está tudo correto **e** pedir para subir.

A branch principal e o fluxo vêm de **Dados do projeto (harness)** no `CLAUDE.md`. Abaixo,
`<principal>` é essa branch.

- **Por PR** — o padrão da empresa. Vale quando o projeto não diz nada.
- **Direto na principal** — só quando o `CLAUDE.md` do projeto disser isso com todas as letras.

## 1. Commitar o próprio trabalho

Antes de puxar, commitar a tarefa com a documentação junto, na mensagem das regras gerais
(Conventional Commits em pt-BR, ID no título). Nunca puxar com alteração solta no working tree.

## 2. Ler o que chegou

```
git fetch origin
git log --oneline HEAD..origin/<principal>
git diff HEAD...origin/<principal> --stat
```

Ler os commits que tocam os mesmos arquivos ou a mesma funcionalidade, e o documento dela.

## 3. Integrar

```
git rebase origin/<principal>
```

Rebase, não merge, para o histórico não encher de commits de merge.

Conflito: resolver mantendo **as duas** alterações funcionando. Nunca descartar o lado do outro
dev (`--ours`/`--theirs` no arquivo inteiro) só para a sua parte passar. Sem entender a intenção
do outro lado, parar e perguntar ao dev. Em índice de documentação, conflito de linha quase sempre
é manter as duas linhas, na ordem do índice.

## 4. Verificar

Rodar o build e a checagem estática do projeto. A funcionalidade do outro dev e a sua precisam
continuar funcionando; se a dele quebrou por causa da sua, corrigir antes de subir.

## 5a. Subir por PR (padrão)

1. Subir a branch da tarefa (criada na etapa 1):

   ```
   git push -u origin <branch da tarefa>
   ```

   Se a branch já estava no GitHub e o rebase mudou o histórico, usar
   `git push --force-with-lease`. **Só na branch da tarefa, nunca na principal.**
2. Abrir o PR para `<principal>` com `gh pr create`:
   - título igual ao do commit principal (`tipo: <ID> o que mudou`);
   - corpo com o parágrafo da motivação, a lista do que mudou, o documento de funcionalidade
     atualizado e o passo a passo de validação que o dev já conferiu;
   - sem assinatura do Claude: nada de "Generated with Claude Code" nem `Co-Authored-By`.
3. Passar o link do PR ao dev. A tarefa continua **Em revisão** até o merge.
4. Pedido de mudança no PR: a tarefa volta para **Fazendo** e o trabalho para a etapa 3 da
   skill **tarefa**.
5. Com o PR aprovado e o merge feito, a tarefa vai para **Feito**. O merge é do dev ou do
   revisor; a IA não faz merge por conta própria.

## 5b. Subir direto na principal (só se o projeto usar)

```
git push origin <principal>
```

Push recusado (alguém subiu no meio): voltar ao passo 2. Com o push feito, a tarefa vai para
**Feito**.

**Nunca `git push --force` na principal, nem `git reset --hard`.**

## 6. Status

Atualizar o status pela skill **status**. Nunca marcar **Feito** antes do merge (PR) ou do push
(direto na principal).

## 7. Fechar a tarefa

Seguir *Ao fechar uma tarefa* das regras gerais: salvar o que importa e sugerir ao dev limpar o
contexto antes da próxima.
