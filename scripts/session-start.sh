#!/bin/sh
# Injeta as regras gerais da empresa no começo de toda sessão do Claude Code.
# Plugin não carrega CLAUDE.md próprio; o hook SessionStart é o jeito de ter regra sempre ativa.
# O stdout deste script entra como contexto (limite de 10 mil caracteres).
cat "$(dirname "$0")/../regras/gerais.md"
