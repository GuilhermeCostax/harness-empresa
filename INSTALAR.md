# Instalar o harness num ambiente novo

Passo a passo para um dev começar a usar o harness numa máquina nova, e para ligar o harness num
projeto novo.

## 1. O que precisa antes

| O quê | Como conferir |
| --- | --- |
| Claude Code instalado e logado na conta do dev | `claude --version` e `/login` dentro do Claude Code |
| Acesso ao repositório `GuilhermeCostax/harness-empresa` (privado) | Pedir ao dono para adicionar o usuário do GitHub como colaborador |
| Git com acesso ao GitHub | `gh auth status` mostra a conta logada, ou `git ls-remote https://github.com/GuilhermeCostax/harness-empresa` funciona |
| GitHub CLI logado (o harness usa para preencher o *Quem* do plano) | `gh api user --jq .login` mostra o usuário |
| Conector Claude Docs ligado (planos e docs de regras ficam lá) | No Claude Code, o plano do projeto abre pelas ferramentas de Docs |

## 2. Instalar o plugin na máquina

Uma vez por máquina:

```
claude plugin marketplace add GuilhermeCostax/harness-empresa
claude plugin install harness@harness-empresa
```

Conferir:

```
claude plugin list
```

A lista mostra `harness@harness-empresa`. Dentro do Claude Code, digitar `/harness:` mostra as
skills `tarefa`, `validar`, `push`, `status` e `documentar`.

## 3. Abrir um projeto que já usa o harness

O projeto tem um `.claude/settings.json` com o marketplace e o plugin. Ao abrir o projeto e
confiar na pasta, o Claude Code já sabe de onde vem o plugin. Se ele avisar que o plugin está
ligado no projeto mas não instalado, rodar o passo 2.

Teste rápido: abrir o Claude Code no projeto e pedir "faz a <ID de uma tarefa>". Ele deve começar
pela etapa 1, lendo a linha da tarefa no plano.

## 4. Atualizar o plugin

Quando alguém mudar o harness:

```
claude plugin marketplace update harness-empresa
claude plugin update harness@harness-empresa
```

Reiniciar o Claude Code depois.

## 5. Ligar o harness num projeto novo

1. Copiar `modelos/CLAUDE-projeto.md` para a raiz do projeto como `CLAUDE.md` e preencher a
   seção **Dados do projeto (harness)**, a stack, a organização do código e as armadilhas.
2. Criar `.claude/settings.json` no projeto:

   ```json
   {
     "extraKnownMarketplaces": {
       "harness-empresa": {
         "source": { "source": "github", "repo": "GuilhermeCostax/harness-empresa" }
       }
     },
     "enabledPlugins": {
       "harness@harness-empresa": true
     }
   }
   ```

3. Criar a pasta de documentação de funcionalidades com o modelo
   (`skills/documentar/modelo.md` vira `<pasta>/_modelo/README.md`).
4. Gerar o `AGENTS.md`, para quem usa o Codex:

   ```
   /caminho/para/harness-empresa/scripts/gerar-agents.sh /caminho/do/projeto
   ```

5. Commitar `CLAUDE.md`, `AGENTS.md` e `.claude/settings.json` juntos.

## 6. Testar uma mudança no plugin antes de subir

Sem instalar nada, só nesta sessão:

```
claude --plugin-dir /caminho/para/harness-empresa
```

E conferir os arquivos do plugin:

```
claude plugin validate /caminho/para/harness-empresa
```
