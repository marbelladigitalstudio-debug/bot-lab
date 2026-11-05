# Repos de trading algorítmico revisados (5-nov-2026)

Método: `git ls-remote` / clon superficial sin blobs (solo LICENSE y fecha del último commit). La API de GitHub no estaba
accesible desde la sesión, así que NO he medido estrellas ni leído el código de cada repo a fondo: la columna "qué aporta"
es conocimiento general del proyecto. Nada se ha instalado ni ejecutado.

| Repo | Licencia | Último commit | Qué aporta | ¿Sirve para nosotros? |
|---|---|---|---|---|
| freqtrade/freqtrade | GPL-3.0 | 2026-11-05 | Bot completo, backtesting, hyperopt, descarga de datos (ccxt) | Referencia de ideas. GPL: no copiar código; sí reescribir ideas |
| freqtrade/freqtrade-strategies | GPL-3.0 | 2026-09-08 | Colección de estrategias de ejemplo (indicadores técnicos) | Fuente de ideas (Supertrend, etc.). La propia colección avisa de que están sobreajustadas |
| hummingbot/hummingbot | Apache-2.0 | 2026-09-22 | Market making y arbitraje, conectores a exchanges (incl. Hyperliquid) | Útil si se llegara a market making; requiere operar en vivo y datos de libro. Hoy no |
| jesse-ai/jesse | MIT | 2026-11-03 | Framework de backtest/optimización para cripto | Ideas de indicadores; no aporta datos que no tengamos |
| polakowo/vectorbt | Apache-2.0 + Commons Clause | 2026-11-03 | Backtest vectorizado muy rápido | La Commons Clause prohíbe vender el software; no lo necesitamos (nuestro motor ya es vectorizado). No usar |
| mementum/backtrader | GPL-3.0 | 2023-04-19 | Backtest clásico por eventos | Abandonado; sin interés |
| nautechsystems/nautilus_trader | LGPL-3.0 | 2026-11-05 | Motor de alto rendimiento de ejecución y backtest | Excesivo para simulación diaria; útil si algún día se pasa a ejecución real |
| QuantConnect/Lean | Apache-2.0 | 2026-11-04 | Motor institucional multi-activo | Referencia metodológica; pesado |
| ccxt/ccxt | MIT | 2026-11-04 | API unificada de ~100 exchanges (datos históricos) | Útil para descargar datos de otros exchanges si hay red. Instalar con versión fija |
| hyperliquid-dex/hyperliquid-python-sdk | MIT | 2026-06-04 | SDK oficial de Hyperliquid | Solo para ejecución; nosotros leemos la API pública. No pide claves si solo se lee |
| microsoft/qlib | MIT | 2026-10-08 | Plataforma de investigación cuantitativa con ML (factores, validación temporal) | Ideas de evaluación (IC, rolling); pensado para bolsa |
| AI4Finance-Foundation/FinRL | MIT | 2026-10-25 | Aprendizaje por refuerzo para trading | Muy propenso a sobreajuste con 180 días; no |
| twopirllc/pandas-ta | (no accesible por git; PyPI no declara licencia clara) | — | ~130 indicadores | No se usa: sin licencia verificable. Los indicadores son fórmulas públicas y se reescriben a mano |

## Conclusión
- Ningún repo aporta una ventaja por sí mismo; las "estrategias probadas" de estos repos son indicadores técnicos clásicos
  que ya están en gran parte en `estrategias.py`.
- Con licencia GPL (freqtrade, strategies, backtrader) solo se reescriben ideas/fórmulas públicas desde cero, sin copiar código.
- Lo único que cambiaría el juego sería más datos (años, libro de órdenes, más mercados), no más indicadores.
