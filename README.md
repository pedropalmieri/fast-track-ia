# Fast Track IA

Repositório de estudos e exercícios da trilha de Inteligência Artificial da Compass UOL.

## Sobre

Este projeto acompanha a evolução dos conhecimentos desenvolvidos durante a trilha, reunindo anotações, exemplos práticos e atividades em um único lugar.

## Objetivos

- Consolidar os fundamentos de Inteligência Artificial.
- Registrar aprendizados e referências importantes.
- Praticar os conceitos por meio de exercícios e pequenos projetos.
- Acompanhar a evolução do conteúdo ao longo da formação.

## Organização

O conteúdo será organizado por módulos ou temas à medida que novos materiais forem adicionados ao repositório.

## Status

Em desenvolvimento, acompanhando o andamento da trilha de estudos.

## Como acompanhar

Consulte os arquivos e diretórios deste repositório para acompanhar os estudos, exercícios e materiais produzidos durante a formação.

## Autoria

Projeto desenvolvido como parte da trilha de Inteligência Artificial da Compass UOL.

## Primeiro checkpoint: Monitoramento da Fauna

Este repositorio inclui uma analise reproduzivel dos cinco desafios do checkpoint.

### Executar

1. Crie um ambiente virtual e instale as dependencias:

	```bash
	python3 -m venv .venv
	source .venv/bin/activate
	pip install -r requirements.txt
	```

2. Gere o relatorio dentro do checkpoint organizad:

	```bash
	python3 checkpoints/01-monitoramento-da-fauna/analise_fauna.py
	```

O script lê o dataset em `checkpoints/01-monitoramento-da-fauna/dataset_monitoramento_fauna.json`, trata temperatura e umidade, preserva valores ausentes e grava o relatório em `checkpoints/01-monitoramento-da-fauna/relatorio_monitoramento_fauna.md`.
