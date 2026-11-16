#!/bin/sh
# Gera o AGENTS.md de um projeto para o Codex e outras ferramentas sem o plugin.
# Junta o CLAUDE.md do projeto, as regras gerais e o texto de cada skill, para quem não usa o
# Claude Code seguir exatamente o mesmo processo. O AGENTS.md não é editado à mão: muda o
# CLAUDE.md do projeto ou o plugin e roda este script de novo.
#
# Uso: scripts/gerar-agents.sh <pasta do projeto>
set -eu

raiz="$(cd "$(dirname "$0")/.." && pwd)"
projeto="${1:?uso: gerar-agents.sh <pasta do projeto>}"
saida="$projeto/AGENTS.md"

[ -f "$projeto/CLAUDE.md" ] || { echo "sem CLAUDE.md em $projeto" >&2; exit 1; }

# Tira o frontmatter (entre as duas primeiras linhas ---) e troca $ARGUMENTS por <ID>.
corpo_da_skill() {
  awk 'NR==1 && $0=="---" {fm=1; next} fm && $0=="---" {fm=0; next} !fm' "$1" |
    sed 's/\$ARGUMENTS/<ID>/g'
}

{
  echo "<!-- Gerado por harness-empresa/scripts/gerar-agents.sh. Não editar à mão: mude o CLAUDE.md"
  echo "     do projeto ou o plugin harness e gere de novo. -->"
  echo
  echo "Este arquivo junta as regras do projeto, as regras gerais da empresa e as skills do plugin"
  echo "harness. Onde o texto diz \"skill X\", siga a seção \"Skill X\" deste arquivo."
  echo
  cat "$projeto/CLAUDE.md"
  echo
  cat "$raiz/regras/gerais.md"
  for skill in tarefa validar push status documentar; do
    echo
    echo "# Skill $skill"
    echo
    corpo_da_skill "$raiz/skills/$skill/SKILL.md" | sed '1,/^# /{/^# /d;}'
  done
} | cat -s > "$saida"

echo "gerado: $saida ($(wc -l < "$saida" | tr -d ' ') linhas)"
