from pathlib import Path

import pandas as pd


ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "dataset_monitoramento_fauna.json"
REPORT_PATH = ROOT / "relatorio_monitoramento_fauna.md"

CAMERA_AREAS = {
    **dict.fromkeys(["CAM01", "CAM02", "CAM03", "CAM04"], "Cerrado aberto"),
    **dict.fromkeys(["CAM05", "CAM06", "CAM07", "CAM08"], "Mata de galeria"),
    **dict.fromkeys(["CAM09", "CAM10", "CAM11", "CAM12"], "Veredas e areas umidas"),
}


def format_number(value, decimals=1):
    return f"{value:.{decimals}f}".replace(".", ",")


def load_data():
    dataframe = pd.read_json(DATA_PATH)
    dataframe["data_hora_inicio"] = pd.to_datetime(dataframe["data_hora_inicio"])
    dataframe["hora"] = dataframe["data_hora_inicio"].dt.hour
    dataframe["temperatura_c"] = pd.to_numeric(
        dataframe["temperatura_c"].str.replace(" °C", "", regex=False),
        errors="coerce",
    )
    dataframe["umidade_pct"] = pd.to_numeric(
        dataframe["umidade_pct"].str.replace("%", "", regex=False),
        errors="coerce",
    )
    dataframe["area"] = dataframe["id_camera"].map(CAMERA_AREAS)
    dataframe["periodo"] = pd.cut(
        dataframe["hora"],
        bins=[-1, 5, 11, 17, 23],
        labels=["Madrugada (00h-05h)", "Manha (06h-11h)", "Tarde (12h-17h)", "Noite (18h-23h)"],
    )
    dataframe["faixa_umidade"] = pd.cut(
        dataframe["umidade_pct"],
        bins=[-float("inf"), 60, 80, float("inf")],
        labels=["Baixa (<60%)", "Media (60%-79,9%)", "Alta (>=80%)"],
    )
    return dataframe


def counts_table(series):
    return series.value_counts().reindex(series.cat.categories, fill_value=0)


def build_report(dataframe):
    capivaras = dataframe[dataframe["especie"] == "Capivara"]
    capybara_mean = capivaras["individuos"].mean()
    solitary = int((capivaras["individuos"] == 1).sum())
    grouped = int((capivaras["individuos"] > 1).sum())

    species_counts = dataframe["especie"].value_counts()
    selected_species = species_counts.head(3).index.tolist()
    activity = dataframe[dataframe["especie"].isin(selected_species)].groupby(
        ["especie", "periodo"], observed=False
    ).size().unstack(fill_value=0)

    humidity = dataframe.dropna(subset=["umidade_pct"])
    humidity_counts = counts_table(humidity["faixa_umidade"])
    amphibians = humidity[humidity["grupo"] == "Anfíbio"]
    amphibian_counts = counts_table(amphibians["faixa_umidade"])
    amphibian_rate = (amphibian_counts / humidity_counts * 100).fillna(0)

    camera_summary = dataframe.groupby(["id_camera", "area"], observed=False).agg(
        registros=("id_registro", "count"), especies=("especie", "nunique")
    ).reset_index().sort_values(["registros", "especies"], ascending=False)

    jaguars = dataframe[dataframe["especie"] == "Onça-pintada"]
    jaguar_cameras = jaguars["id_camera"].value_counts()
    jaguar_periods = jaguars["periodo"].value_counts().reindex(
        dataframe["periodo"].cat.categories, fill_value=0
    )
    jaguar_areas = jaguars["area"].value_counts()

    lines = [
        "# Relatorio - Monitoramento da Fauna",
        "",
        "Analise reproduzivel dos 5.000 registros entre 01/05/2026 e 30/05/2026.",
        "",
        "## Preparacao dos dados",
        "",
        f"- Registros analisados: **{len(dataframe):,}**".replace(",", "."),
        f"- Temperatura convertida para numero; umidade convertida para numero e mantida ausente quando nula ({int(dataframe['umidade_pct'].isna().sum())} registros).",
        "- Periodos: madrugada (00h-05h), manha (06h-11h), tarde (12h-17h) e noite (18h-23h).",
        "- Faixas de umidade: baixa (<60%), media (60%-79,9%) e alta (>=80%).",
        "",
        "## Desafio 1 - Capivaras",
        "",
        f"A media foi de **{format_number(capybara_mean)} individuos por registro**, considerando {len(capivaras)} registros.",
        f"Foram {solitary} registros solitarios ({solitary / len(capivaras) * 100:.1f}%) e {grouped} em grupo ({grouped / len(capivaras) * 100:.1f}%). Portanto, a maior parte dos registros envolve **grupos**.",
        "",
        "## Desafio 2 - Atividade ao longo do dia",
        "",
        f"Foram escolhidas as tres especies mais registradas: {', '.join(selected_species)}.",
        "",
        "| Especie | Madrugada | Manha | Tarde | Noite | Periodo de maior ocorrencia |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for species in selected_species:
        row = activity.loc[species]
        peak = row.idxmax()
        lines.append(f"| {species} | {row.iloc[0]} | {row.iloc[1]} | {row.iloc[2]} | {row.iloc[3]} | {peak} |")

    lines.extend([
        "",
        "A comparacao mostra que os horarios de pico variam entre especies; por isso, uma rotina de campo deve considerar a especie-alvo, e nao apenas um horario unico para toda a fauna.",
        "",
        "## Desafio 3 - Umidade e anfibios",
        "",
        "| Faixa de umidade | Registros validos | Registros de anfibios | Proporcao de anfibios na faixa |",
        "|---|---:|---:|---:|",
    ])
    for humidity_band in humidity_counts.index:
        lines.append(f"| {humidity_band} | {humidity_counts[humidity_band]} | {amphibian_counts[humidity_band]} | {format_number(amphibian_rate[humidity_band])}% |")
    highest_rate_band = amphibian_rate.idxmax()
    lines.extend([
        "",
        f"A maior proporcao de anfibios ocorreu na faixa **{highest_rate_band}** ({format_number(amphibian_rate[highest_rate_band])}%). Assim, neste conjunto de dados, a umidade mais alta esta associada a maior frequencia relativa de registros de anfibios. A associacao nao prova causalidade e deve ser interpretada junto com horario, camera e esforco de amostragem.",
        "",
        "## Desafio 4 - Cameras prioritarias",
        "",
        "| Camera | Area | Registros | Especies distintas |",
        "|---|---|---:|---:|",
    ])
    for row in camera_summary.head(5).itertuples(index=False):
        lines.append(f"| {row.id_camera} | {row.area} | {row.registros} | {row.especies} |")
    top_cameras = camera_summary.head(3)["id_camera"].tolist()
    top_areas = camera_summary.head(3)["area"].value_counts()
    lines.extend([
        "",
        f"Recomendo priorizar {', '.join(top_cameras)}, que combinam alto volume de registros e diversidade. Entre as tres primeiras, a area mais representada e **{top_areas.idxmax()}** ({top_areas.max()} cameras), mas a estrategia deve preservar cobertura das demais areas.",
        "",
        "## Desafio 5 - Onca-pintada",
        "",
        f"Foram encontrados {len(jaguars)} registros de onca-pintada. As cameras mais indicadas sao **{', '.join(jaguar_cameras.head(3).index)}**, com {', '.join(str(value) for value in jaguar_cameras.head(3).tolist())} registros, respectivamente.",
        f"A area com mais registros foi **{jaguar_areas.idxmax()}** ({jaguar_areas.max()} registros). O periodo de maior ocorrencia foi **{jaguar_periods.idxmax()}** ({jaguar_periods.max()} registros). Eu concentraria o proximo monitoramento nesses pontos e horarios, mantendo cameras de apoio porque ausencia de deteccao nao significa ausencia da especie.",
        "",
        "## Observacao",
        "",
        "Os resultados descrevem eventos de deteccao, nao abundancia populacional. Diferencas entre cameras tambem podem refletir posicionamento, cobertura, visibilidade e funcionamento dos equipamentos.",
    ])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    report = build_report(load_data())
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Relatorio salvo em {REPORT_PATH}")