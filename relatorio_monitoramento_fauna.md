# Relatório - Monitoramento da Fauna

Análise reprodutível dos 5,000 registros entre 01/05/2026 e 30/05/2026.

## Preparação dos dados

- Registros analisados: **5.000**
- Temperatura convertida para número; umidade convertida para número e mantida ausente quando nula (175 registros).
- Períodos: madrugada (00h-05h), manhã (06h-11h), tarde (12h-17h) e noite (18h-23h).
- Faixas de umidade: baixa (<60%), média (60%-79,9%) e alta (>=80%).

## Desafio 1 - Capivaras

A média foi de **6,0 indivíduos por registro**, considerando 731 registros.
Foram 6 registros solitários (0.8%) e 725 em grupo (99.2%). Portanto, a maior parte dos registros envolve **grupos**.

## Desafio 2 - Atividade ao longo do dia

Foram escolhidas as três espécies mais registradas: Capivara, Sapo-cururu, Ema.

| Espécie | Madrugada | Manhã | Tarde | Noite | Período de maior ocorrência |
|---|---:|---:|---:|---:|---|
| Capivara | 72 | 292 | 283 | 84 | Manhã (06h-11h) |
| Sapo-cururu | 250 | 54 | 51 | 209 | Madrugada (00h-05h) |
| Ema | 51 | 217 | 230 | 53 | Tarde (12h-17h) |

A comparação mostra que os horários de pico variam entre espécies; por isso, uma rotina de campo deve considerar a espécie-alvo e não apenas um único horário para toda a fauna.

## Desafio 3 - Umidade e anfíbios

| Faixa de umidade | Registros válidos | Registros de anfíbios | Proporção de anfíbios na faixa |
|---|---:|---:|---:|
| Baixa (<60%) | 477 | 21 | 4,4% |
| Média (60%-79,9%) | 2331 | 389 | 16,7% |
| Alta (>=80%) | 2017 | 789 | 39,1% |

A maior proporção de anfíbios ocorreu na faixa **Alta (>=80%)** (39,1%).Assim, neste conjunto de dados, a umidade mais alta está associada à maior frequência relativa de registros de anfíbios. A associação não prova causalidade e deve ser interpretada junto com horário, câmera e esforço de amostragem.

## Desafio 4 - Câmeras prioritárias

| Câmera | Área | Registros | Espécies distintas |
|---|---|---:|---:|
| CAM09 | Veredas e áreas úmidas | 523 | 12 |
| CAM12 | Veredas e áreas úmidas | 504 | 13 |
| CAM10 | Veredas e áreas úmidas | 474 | 12 |
| CAM02 | Cerrado aberto | 471 | 12 |
| CAM04 | Cerrado aberto | 442 | 12 |

Recomendo priorizar CAM09, CAM12, CAM10, que combinam alto volume de registros e diversidade. Entre as três primeiras, a área mais representada é **Veredas e áreas úmidas** (3 câmeras), mas a estratégia deve preservar a cobertura das demais áreas.

## Desafio 5 - Onça-pintada

Foram encontrados 20 registros de onça-pintada. As câmeras mais indicadas são **CAM06, CAM08, CAM07**, com 6, 5, 4 registros, respectivamente.
A área com mais registros foi **Mata de galeria** (17 registros). O período de maior ocorrência foi **Noite (18h-23h)** (10 registros). Eu concentraria o próximo monitoramento nesses pontos e horários, mantendo câmeras de apoio porque ausência de detecção não significa ausência da espécie.

## Observação

Os resultados descrevem eventos de detecção, não abundância populacional. Diferenças entre câmeras também podem refletir posicionamento, cobertura, visibilidade e funcionamento dos equipamentos.
