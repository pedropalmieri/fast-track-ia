from pathlib import Path

import pandas as pd


# 1) Definição dos caminhos principais do projeto para localizar o dataset e salvar o relatorio final.
# Mantemos compatibilidade com os layouts antigos e atuais do checkpoint.
ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "dataset_monitoramento_fauna.json"
if not DATA_PATH.exists():
    DATA_PATH = ROOT / "data" / "dataset_monitoramento_fauna.json"
REPORT_PATH = ROOT / "relatorio_monitoramento_fauna.md"

# 2) Mapeamento de cada câmera para a área de habitat correspondente.
# Isso facilita a análise por ambiente e a comparação entre regiões monitoradas.
CAMERA_AREAS = {
    **dict.fromkeys(["CAM01", "CAM02", "CAM03", "CAM04"], "Cerrado aberto"),
    **dict.fromkeys(["CAM05", "CAM06", "CAM07", "CAM08"], "Mata de galeria"),
    **dict.fromkeys(["CAM09", "CAM10", "CAM11", "CAM12"], "Veredas e áreas úmidas"),
}


def format_number(value, decimals=1):
    """Formatamos números para apresentação em texto, trocando ponto por vírgula."""
    return f"{value:.{decimals}f}".replace(".", ",")


def load_data():
    """Etapa de carregamento e limpeza do dataset antes da análise estatística."""
    # Leitura do arquivo JSON gerado pelo monitoramento da fauna.
    dataframe = pd.read_json(DATA_PATH)

    # Convertendo a coluna de data/hora para datetime para podermos extrair o horário.
    dataframe["data_hora_inicio"] = pd.to_datetime(dataframe["data_hora_inicio"])
    dataframe["hora"] = dataframe["data_hora_inicio"].dt.hour

    # Ajustando valores de temperatura e umidade, removendo sufixos e convertendo para numérico.
    # O parâmetro errors='coerce' mantém valores nulos caso a conversão falhe.
    dataframe["temperatura_c"] = pd.to_numeric(
        dataframe["temperatura_c"].str.replace(" °C", "", regex=False),
        errors="coerce",
    )
    dataframe["umidade_pct"] = pd.to_numeric(
        dataframe["umidade_pct"].str.replace("%", "", regex=False),
        errors="coerce",
    )

    # Realizando o mapeamento das câmeras para as áreas ecológicas para contextualizar os registros.
    dataframe["area"] = dataframe["id_camera"].map(CAMERA_AREAS)

    # Classificação de cada registro por período do dia considerando a hora de ocorrência.
    dataframe["periodo"] = pd.cut(
        dataframe["hora"],
        bins=[-1, 5, 11, 17, 23],
        labels=["Madrugada (00h-05h)", "Manhã (06h-11h)", "Tarde (12h-17h)", "Noite (18h-23h)"],
    )

    # Agrupamento da umidade em faixas para facilitar a comparação entre ambientes mais secos e úmidos.
    dataframe["faixa_umidade"] = pd.cut(
        dataframe["umidade_pct"],
        bins=[-float("inf"), 60, 80, float("inf")],
        labels=["Baixa (<60%)", "Média (60%-79,9%)", "Alta (>=80%)"],
    )

    return dataframe


def counts_table(series):
    """Cria uma tabela de contagem com categorias definidas mesmo quando alguma categoria não aparece."""
    # Reindexa para manter todas as categorias da série, preenchendo faltantes com zero.
    return series.value_counts().reindex(series.cat.categories, fill_value=0)


def build_report(dataframe):
    """Agrupa os indicadores principais e monta o texto final do relatório em Markdown."""

    # --- Desafio 1: Capivaras ---
    # Filtrando apenas os registros de capivaras para analisar o comportamento social da espécie.
    capivaras = dataframe[dataframe["especie"] == "Capivara"]
    capybara_mean = capivaras["individuos"].mean()
    solitary = int((capivaras["individuos"] == 1).sum())
    grouped = int((capivaras["individuos"] > 1).sum())

    # --- Desafio 2: Atividade ao longo do dia ---
    # Identificando as três espécies mais frequentes e calculamos a sua atividade por período.
    species_counts = dataframe["especie"].value_counts()
    selected_species = species_counts.head(3).index.tolist()
    activity = dataframe[dataframe["especie"].isin(selected_species)].groupby(["especie", "periodo"], observed=False).size().unstack(fill_value=0)

    # --- Desafio 3: Umidade e anfíbios ---
    # Removendo registros sem umidade para focar na relação entre umidade e ocorrência de anfíbios.
    humidity = dataframe.dropna(subset=["umidade_pct"])
    humidity_counts = counts_table(humidity["faixa_umidade"])
    amphibians = humidity[humidity["grupo"] == "Anfíbio"]
    amphibian_counts = counts_table(amphibians["faixa_umidade"])
    amphibian_rate = (amphibian_counts / humidity_counts * 100).fillna(0)

    # --- Desafio 4: Câmeras prioritárias ---
    # Agrupando os registros por câmera e área para analisar volume e diversidade observados.
    camera_summary = dataframe.groupby(["id_camera", "area"], observed=False).agg(
        registros=("id_registro", "count"), especies=("especie", "nunique")
    ).reset_index().sort_values(["registros", "especies"], ascending=False)

    # --- Desafio 5: Onça-pintada ---
    # Foco na espécie de maior interesse para avaliar onde, quando e em quais câmeras ela aparece mais.
    jaguars = dataframe[dataframe["especie"] == "Onça-pintada"]
    jaguar_cameras = jaguars["id_camera"].value_counts()
    jaguar_periods = jaguars["periodo"].value_counts().reindex(
        dataframe["periodo"].cat.categories, fill_value=0
    )
    jaguar_areas = jaguars["area"].value_counts()

    # Montando o texto do relatório em listas de linhas para facilitar a escrita final em Markdown.
    lines = [
        "# Relatório - Monitoramento da Fauna",
        "",
        f"Análise reprodutível dos {len(dataframe):,.0f} registros entre 01/05/2026 e 30/05/2026.",
        "",
        "## Preparação dos dados",
        "",
        f"- Registros analisados: **{len(dataframe):,}**".replace(",", "."),
        f"- Temperatura convertida para número; umidade convertida para número e mantida ausente quando nula ({int(dataframe['umidade_pct'].isna().sum())} registros).",
        "- Períodos: madrugada (00h-05h), manhã (06h-11h), tarde (12h-17h) e noite (18h-23h).",
        "- Faixas de umidade: baixa (<60%), média (60%-79,9%) e alta (>=80%).",
        "",
        "## Desafio 1 - Capivaras",
        "",
        f"A média foi de **{format_number(capybara_mean)} indivíduos por registro**, considerando {len(capivaras)} registros.",
        f"Foram {solitary} registros solitários ({solitary / len(capivaras) * 100:.1f}%) e {grouped} em grupo ({grouped / len(capivaras) * 100:.1f}%). Portanto, a maior parte dos registros envolve **grupos**.",
        "",
        "## Desafio 2 - Atividade ao longo do dia",
        "",
        f"Foram escolhidas as três espécies mais registradas: {', '.join(selected_species)}.",
        "",
        "| Espécie | Madrugada | Manhã | Tarde | Noite | Período de maior ocorrência |",
        "|---|---:|---:|---:|---:|---|",
    ]

    # Repetindo sobre as espécies mais frequentes para montar a tabela de atividade por período do dia.
    for species in selected_species:
        row = activity.loc[species]
        peak = row.idxmax()
        lines.append(f"| {species} | {row.iloc[0]} | {row.iloc[1]} | {row.iloc[2]} | {row.iloc[3]} | {peak} |")

    lines.extend([
        "",
        "A comparação mostra que os horários de pico variam entre espécies; por isso, uma rotina de campo deve considerar a espécie-alvo e não apenas um único horário para toda a fauna.",
        "",
        "## Desafio 3 - Umidade e anfíbios",
        "",
        "| Faixa de umidade | Registros válidos | Registros de anfíbios | Proporção de anfíbios na faixa |",
        "|---|---:|---:|---:|",
    ])

    # Montando a comparação de anfíbios por faixa de umidade para identificar o ambiente mais relevante.
    for humidity_band in humidity_counts.index:
        lines.append(f"| {humidity_band} | {humidity_counts[humidity_band]} | {amphibian_counts[humidity_band]} | {format_number(amphibian_rate[humidity_band])}% |")
    highest_rate_band = amphibian_rate.idxmax()
    lines.extend([
        "",
        f"A maior proporção de anfíbios ocorreu na faixa **{highest_rate_band}** ({format_number(amphibian_rate[highest_rate_band])}%). "
        f"Assim, neste conjunto de dados, a umidade mais alta está associada à maior frequência relativa de registros de anfíbios. "
        f"A associação não prova causalidade e deve ser interpretada junto com horário, câmera e esforço de amostragem.",
        "",
        "## Desafio 4 - Câmeras prioritárias",
        "",
        "| Câmera | Área | Registros | Espécies distintas |",
        "|---|---|---:|---:|",
    ])

    # Selecionando as câmeras com maior volume de registros para recomendar foco de monitoramento.
    for row in camera_summary.head(5).itertuples(index=False):
        lines.append(f"| {row.id_camera} | {row.area} | {row.registros} | {row.especies} |")
    top_cameras = camera_summary.head(3)["id_camera"].tolist()
    top_areas = camera_summary.head(3)["area"].value_counts()
    lines.extend([
        "",
        f"Recomendo priorizar {', '.join(top_cameras)}, que combinam alto volume de registros e diversidade. Entre as três primeiras, a área mais representada é **{top_areas.idxmax()}** ({top_areas.max()} câmeras), mas a estratégia deve preservar a cobertura das demais áreas.",
        "",
        "## Desafio 5 - Onça-pintada",
        "",
        f"Foram encontrados {len(jaguars)} registros de onça-pintada. As câmeras mais indicadas são **{', '.join(jaguar_cameras.head(3).index)}**, com {', '.join(str(value) for value in jaguar_cameras.head(3).tolist())} registros, respectivamente.",
        f"A área com mais registros foi **{jaguar_areas.idxmax()}** ({jaguar_areas.max()} registros). O período de maior ocorrência foi **{jaguar_periods.idxmax()}** ({jaguar_periods.max()} registros). Eu concentraria o próximo monitoramento nesses pontos e horários, mantendo câmeras de apoio porque ausência de detecção não significa ausência da espécie.",
        "",
        "## Observação",
        "",
        "Os resultados descrevem eventos de detecção, não abundância populacional. Diferenças entre câmeras também podem refletir posicionamento, cobertura, visibilidade e funcionamento dos equipamentos.",
    ])

    # Finalizando juntando todas as linhas do relatório em um único texto Markdown.
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    # Etapa final: executa a pipeline completa e salva o relatório no diretório do projeto.
    report = build_report(load_data())
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Relatorio salvo em {REPORT_PATH}")