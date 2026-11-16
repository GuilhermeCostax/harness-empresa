---
name: push
description: Etapa 7 do processo da empresa. Commita a tarefa, confere o que os outros devs subiram, integra sem quebrar o trabalho deles e sobe para a branch principal, marcando a tarefa como Feito. Use só quando o dev disser que a tarefa está correta e pedir para commitar, subir ou dar push.
argument-hint: <ID da tarefa>
---

# Subir a tarefa $ARGUMENTS

Só rodar depois de o dev dizer que está tudo correto **e** pedir para subir. A branch principal e
o fluxo (direto nela ou por PR) vêm de **Dados do projeto (harness)** no `CLAUDE.md`. Abaixo,
`<principal>` é essa branch.

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
git pull --rebase origin <principal>
```

Rebase, não merge, para a branch não encher de commits de merge.

Conflito: resolver mantendo **as duas** alterações funcionando. Nunca descartar o lado do outro
dev (`--ours`/`--theirs` no arquivo inteiro) só para a sua parte passar. Sem entender a intenção
do outro lado, parar e perguntar ao dev. Em índice de documentação, conflito de linha quase sempre
é manter as duas linhas, na ordem do índice.

## 4. Verificar

Rodar o build e a checagem estática do projeto. A funcionalidade do outro dev e a sua precisam
continuar funcionando; se a dele quebrou por causa da sua, corrigir antes de subir.

## 5. Subir

```
git push origin <principal>
```

Push recusado (alguém subiu no meio): voltar ao passo 2.

**Nunca `git push --force` nem `git reset --hard`.**

## 6. Status

Com o push feito, a tarefa vai para **Feito** e o módulo é conferido (skill **status**). Nunca
marcar **Feito** antes do push.
