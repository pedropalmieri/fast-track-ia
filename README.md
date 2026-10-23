# Fast Track IA

Repositório de estudos, checkpoints e desafios da trilha de Inteligência
Artificial da Compass UOL.

## Conteúdo

```text
.
├── checkpoints/
│   └── 01-monitoramento-da-fauna/
│       ├── analise_fauna.py
│       ├── checkpoint_monitoramento_fauna.md
│       ├── dataset_monitoramento_fauna.json
│       └── relatorio_monitoramento_fauna.md
└── desafios/
    └── analise-credito/
        ├── analise_credito.ipynb
        ├── dataset.csv
        └── README.md
```

## Requisitos

- Python 3.9 ou superior
- `pip`

Crie e ative um ambiente virtual na raiz do repositório e instale as
dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No Windows, ative o ambiente com `.venv\Scripts\activate`.

## Análises

### Monitoramento da fauna

Execute a partir da raiz do repositório:

```bash
python checkpoints/01-monitoramento-da-fauna/analise_fauna.py
```

O script lê `dataset_monitoramento_fauna.json` e atualiza
`relatorio_monitoramento_fauna.md` no mesmo diretório.

### Análise de crédito

Inicie o Jupyter no diretório do desafio para que o notebook encontre o dataset
usando o caminho relativo configurado:

```bash
cd desafios/analise-credito
jupyter lab analise_credito.ipynb
```

No Jupyter, execute todas as células em ordem. O contexto, os dados e as etapas
do desafio estão descritos em [desafios/analise-credito/README.md](desafios/analise-credito/README.md).
