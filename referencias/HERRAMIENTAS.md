# Caja de herramientas del bot (5-nov-2026)

Todo lo que el bot puede necesitar en el futuro, por necesidad. Cada herramienta tiene licencia comprobada, versión
fijada (`requisitos/`) y, cuando hace falta, un adaptador nuestro en `lab/herramientas/`. **El laboratorio sigue
funcionando solo con numpy y pandas**: lo demás es opcional y cada adaptador avisa si falta su librería.

Instalación (en el portátil; en la nube la red a los datos está bloqueada):
```bash
pip install -r requisitos/todo.txt
```
O el entorno exacto probado (115 paquetes):
```bash
pip install -r requisitos/bloqueo.txt
```

## 1. Datos
| Necesidad | Herramienta | Licencia | Adaptador | Estado |
|---|---|---|---|---|
| Historia larga de cripto (2019→hoy, 1h/4h, funding) | ccxt 4.5.92 | MIT | `herramientas/descarga_ccxt.py` → `LAB_BASE=base_binanceusdm.pkl.gz` | Paginación probada con exchange simulado; sin red real aquí |
| Hyperliquid (lectura) | hyperliquid-python-sdk 0.24.0 | MIT | `datos.py` ya usa la API pública | Solo `Info`; **nunca** `Exchange` ni claves |
| S&P 500, ETFs sectoriales, VIX | yfinance 1.7.0 | Apache-2.0 | `herramientas/descarga_acciones.py` | Sin red aquí. 1.8.0 choca con ccxt (cffi) |
| Macro (tipos, FRED) | pandas-datareader 0.11.1 | BSD-3 | — | Pendiente |
| Guardar bases grandes | pyarrow 26.0.1 | Apache-2.0 | — | Cuando la base pase de ~500 MB |

## 2. Noticias y sentimiento
| Necesidad | Herramienta | Licencia | Adaptador | Estado |
|---|---|---|---|---|
| Titulares RSS (CoinDesk, Cointelegraph, Decrypt, The Block, Yahoo) | feedparser 6.0.14 | BSD-2 | `herramientas/noticias.py` | Se acumulan a diario en `lab/datos/noticias.pkl.gz` |
| Noticias mundiales con fecha | gdeltdoc 1.12.0 (GDELT DOC 2.0) | MIT | idem | Gratis, sin claves |
| Sentimiento rápido | vaderSentiment 3.3.2 | MIT | idem | Probado. **Flojo en finanzas**: "Bitcoin surges to record high" = 0,00 |
| Sentimiento financiero bueno | transformers 5.22.1 + FinBERT (ProsusAI) | Apache-2.0 | — | Pesado (~2 GB). Siguiente paso si las noticias acumuladas lo justifican |
| LLM financiero | FinGPT (`terceros/fingpt`) | MIT | — | Referencia |
| Agentes LLM que "deciden" | ai-hedge-fund (MIT), TradingAgents (Apache-2.0) en `terceros/` | — | — | Solo para leer. Piden claves de LLM y de datos: **no ejecutar** sin revisarlos. Sin evidencia fuera de muestra |

Regla de oro con las noticias: un titular cuenta en la barra en cuyo **cierre** ya se conocía, más una barra de margen
(`sentimiento_panel(..., retraso=1)`). Superado el test de truncado. Problema real: no hay archivo histórico gratis de
titulares de cripto con hora fiable, así que la señal solo se puede validar **hacia delante**, acumulando desde hoy.

## 3. Régimen ("usar una estrategia u otra según cómo se vea el mercado")
| Herramienta | Licencia | Dónde | Estado |
|---|---|---|---|
| hmmlearn 0.3.3 (HMM gaussiano) | BSD | `herramientas/regimen.py`, familia `hmm_regimen` en `lab/extra_hmm.py` | Filtro hacia delante propio. El test de truncado **cazó un fallo** (el arranque dependía de la longitud total) y ya está corregido |
| ruptures 1.1.10 | BSD-2 | `herramientas/regimen.py` | Usa toda la serie: **solo diagnóstico, nunca señal** |
| Ratio de eficiencia de Kaufman | fórmula | `lab/extra_regimen.py` | Sin dependencias |

## 4. Validación (lo más importante)
| Herramienta | Licencia | Para qué | Estado |
|---|---|---|---|
| arch 8.0.0 (`arch.bootstrap.SPA`) | NCSA | Referencia del SPA de Hansen | `herramientas/contraste_spa.py`: nuestro SPA y el de arch llegan a las mismas conclusiones (sintético y reserva real) |
| skfolio 1.12.5 | BSD-3 | CombinatorialPurgedCV (López de Prado), carteras | Instalado; pendiente de integrar como alternativa al PBO |
| scikit-learn 1.9.1 | BSD-3 | `TimeSeriesSplit` y modelos | — |
| statsmodels 0.15.0 | BSD-3 | Cointegración para pares, ADF | Pendiente: familia de pares |
| optuna 5.0.0 | MIT | Búsqueda de parámetros | Usar con cuidado: más búsqueda = DSR más exigente |
| lightgbm 4.7.0 | MIT | Modelos de señal con ML | Solo con 2+ años de datos |
| ta 0.11.0 | MIT | ~40 indicadores | Comprobar con el test de truncado antes de usarlos |
| quantstats 0.0.86 | Apache-2.0 | Informe HTML de una estrategia | `herramientas/informe_quantstats.py` |

## 5. Operativa futura (NO se usa hoy)
| Herramienta | Licencia | Para qué |
|---|---|---|
| apprise 2.1.0 | BSD-2 | Avisos por Telegram, correo o Discord (`herramientas/avisos.py`; la URL va en la variable `BOT_AVISOS`) |
| hummingbot (`terceros/`) | Apache-2.0 | Market making, si algún día hay datos de libro y ventaja demostrada |
| nautilus_trader (`terceros/`) | LGPL-3.0 | Motor de ejecución serio |
| freqtrade (`terceros/`) | GPL-3.0 | Bot completo con modo *dry-run*. Se puede usar como programa; no se copia su código |
| Lean, jesse, qlib, Kronos (`terceros/`) | Apache / MIT | Referencias de diseño y modelos |

## 6. `terceros/`: submódulos fijados a un commit
Son enlaces, no copias: el repo no crece. Para descargar uno solo:
```bash
git submodule update --init --depth 1 terceros/<nombre>
```
**No usar `--recursive` con todo**: Lean, ccxt y nautilus pesan cientos de MB. Lista con commit y licencia en
`referencias/MANIFIESTO.md`.

## Bloqueado desde la nube (5-nov-2026)
Hyperliquid, Binance, Bybit, OKX, Yahoo, Stooq, FRED, GDELT, CoinGecko, RSS de noticias, HuggingFace, arXiv y SSRN
devuelven 403 en el proxy. Funcionan GitHub (git) y PyPI. Por eso **ninguna descarga real se ha probado aquí**:
hay que ejecutarlas una vez en el portátil.
