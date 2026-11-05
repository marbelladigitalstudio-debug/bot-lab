# Manifiesto de código/ideas de terceros

No se ha copiado código de terceros. Las familias de `lab/extra_*.py` son reescrituras propias de fórmulas públicas.

| Fecha | Qué | Origen (repo @ commit) | Licencia | Uso |
|---|---|---|---|---|
| 2026-11-05 | Idea: Supertrend | freqtrade/freqtrade-strategies @ f3340ce11f5bdf62f598522e64d1f5638eaa13f5 | GPL-3.0 | Solo la idea; código reescrito desde la fórmula (ATR) |
| 2026-11-05 | Idea: Keltner/squeeze, Ichimoku, ADX, Vortex | Fórmulas públicas de análisis técnico; revisadas freqtrade-strategies @ mismo commit | GPL-3.0 (repo) / fórmulas libres | Reescritas |

## Submódulos en `terceros/` (5-nov-2026): enlaces fijados, no copias
| Carpeta | Repo | Commit | Licencia |
|---|---|---|---|
| terceros/freqtrade | freqtrade/freqtrade | 0789f5d5c3e7649e2b83f82d65ecb2e1381f02ad | GPL-3.0 |
| terceros/freqtrade-strategies | freqtrade/freqtrade-strategies | f3340ce11f5bdf62f598522e64d1f5638eaa13f5 | GPL-3.0 |
| terceros/hummingbot | hummingbot/hummingbot | 9af100d6822da7d2d0291a906c730ef172284ee2 | Apache-2.0 |
| terceros/nautilus_trader | nautechsystems/nautilus_trader | 44330a5b18044434d269ae7994de8236bf8bc45a | LGPL-3.0 |
| terceros/jesse | jesse-ai/jesse | 8665b253d43af7b06a88c6ebcda7a0b6393ec937 | MIT |
| terceros/lean | QuantConnect/Lean | 49b4aa7022abd38e99e9c7d3ec67929fa7f6d7b8 | Apache-2.0 |
| terceros/hyperliquid-python-sdk | hyperliquid-dex/hyperliquid-python-sdk | 2fdb18f9517675ea03695a0962bd19eece9c83f0 | MIT |
| terceros/ccxt | ccxt/ccxt | 7816a60470453df5bfe53a74df8e51d49019cd89 | MIT |
| terceros/qlib | microsoft/qlib | 54355232463878d2eebb91fe0ee5fa7fa1f5976c | MIT |
| terceros/fingpt | AI4Finance-Foundation/FinGPT | ac5c5443fbeeafad801e7a3c188e4f24cfaad4d8 | MIT |
| terceros/ai-hedge-fund | virattt/ai-hedge-fund | e8655f10453f0c7c0874c8d691ef5ae2d74dab5c | MIT |
| terceros/tradingagents | TauricResearch/TradingAgents | 9fa1196fffbcfd9de5146d2dd2869df84ab99838 | Apache-2.0 |
| terceros/kronos | shiyu-coder/Kronos | 67b630e67f6a18c9e9be918d9b4337c960db1e9a | MIT |
| terceros/arch | bashtage/arch | 88d011adcb18966355345dd32557bb0c4879cede | NCSA |
| terceros/skfolio | skfolio/skfolio | 0db206ed812622088cbd33af2e34a0f4762fa71e | BSD-3 |

## Librerías (pip, versiones en `requisitos/`): se usan como dependencia, no se copia código
ccxt (MIT), hyperliquid-python-sdk (MIT), yfinance (Apache-2.0), pandas-datareader (BSD-3), pyarrow (Apache-2.0),
feedparser (BSD-2), gdeltdoc (MIT), vaderSentiment (MIT), scipy/statsmodels/scikit-learn (BSD-3), arch (NCSA),
hmmlearn (BSD), ruptures (BSD-2), lightgbm (MIT), optuna (MIT), skfolio (BSD-3), ta (MIT), quantstats (Apache-2.0),
apprise (BSD-2). Descartadas: pandas-ta (licencia no verificable; repo no accesible), vectorbt (Commons Clause),
python-telegram-bot (LGPL; apprise basta).
