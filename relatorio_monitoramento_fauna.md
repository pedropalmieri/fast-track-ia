# Relatorio - Monitoramento da Fauna

Analise reproduzivel dos 5.000 registros entre 01/05/2026 e 30/05/2026.

## Preparacao dos dados

- Registros analisados: **5.000**
- Temperatura convertida para numero; umidade convertida para numero e mantida ausente quando nula (175 registros).
- Periodos: madrugada (00h-05h), manha (06h-11h), tarde (12h-17h) e noite (18h-23h).
- Faixas de umidade: baixa (<60%), media (60%-79,9%) e alta (>=80%).

## Desafio 1 - Capivaras

A media foi de **6,0 individuos por registro**, considerando 731 registros.
Foram 6 registros solitarios (0.8%) e 725 em grupo (99.2%). Portanto, a maior parte dos registros envolve **grupos**.

## Desafio 2 - Atividade ao longo do dia

Foram escolhidas as tres especies mais registradas: Capivara, Sapo-cururu, Ema.

| Especie | Madrugada | Manha | Tarde | Noite | Periodo de maior ocorrencia |
|---|---:|---:|---:|---:|---|
| Capivara | 72 | 292 | 283 | 84 | Manha (06h-11h) |
| Sapo-cururu | 250 | 54 | 51 | 209 | Madrugada (00h-05h) |
| Ema | 51 | 217 | 230 | 53 | Tarde (12h-17h) |

A comparacao mostra que os horarios de pico variam entre especies; por isso, uma rotina de campo deve considerar a especie-alvo, e nao apenas um horario unico para toda a fauna.

## Desafio 3 - Umidade e anfibios

| Faixa de umidade | Registros validos | Registros de anfibios | Proporcao de anfibios na faixa |
|---|---:|---:|---:|
| Baixa (<60%) | 477 | 21 | 4,4% |
| Media (60%-79,9%) | 2331 | 389 | 16,7% |
| Alta (>=80%) | 2017 | 789 | 39,1% |

A maior proporcao de anfibios ocorreu na faixa **Alta (>=80%)** (39,1%). Assim, neste conjunto de dados, a umidade mais alta esta associada a maior frequencia relativa de registros de anfibios. A associacao nao prova causalidade e deve ser interpretada junto com horario, camera e esforco de amostragem.

## Desafio 4 - Cameras prioritarias

| Camera | Area | Registros | Especies distintas |
|---|---|---:|---:|
| CAM09 | Veredas e areas umidas | 523 | 12 |
| CAM12 | Veredas e areas umidas | 504 | 13 |
| CAM10 | Veredas e areas umidas | 474 | 12 |
| CAM02 | Cerrado aberto | 471 | 12 |
| CAM04 | Cerrado aberto | 442 | 12 |

Recomendo priorizar CAM09, CAM12, CAM10, que combinam alto volume de registros e diversidade. Entre as tres primeiras, a area mais representada e **Veredas e areas umidas** (3 cameras), mas a estrategia deve preservar cobertura das demais areas.

## Desafio 5 - Onca-pintada

Foram encontrados 20 registros de onca-pintada. As cameras mais indicadas sao **CAM06, CAM08, CAM07**, com 6, 5, 4 registros, respectivamente.
A area com mais registros foi **Mata de galeria** (17 registros). O periodo de maior ocorrencia foi **Noite (18h-23h)** (10 registros). Eu concentraria o proximo monitoramento nesses pontos e horarios, mantendo cameras de apoio porque ausencia de deteccao nao significa ausencia da especie.

## Observacao

Os resultados descrevem eventos de deteccao, nao abundancia populacional. Diferencas entre cameras tambem podem refletir posicionamento, cobertura, visibilidade e funcionamento dos equipamentos.
