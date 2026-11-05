"""
Cambio de regimen (peticion de Miguel, 5-nov-2026): usar una estrategia u otra segun como "se vea" el mercado.
Regimen por moneda con el ratio de eficiencia de Kaufman (ER) sobre n barras:
  ER alto  -> mercado en tendencia -> seguir tendencia (precio vs EMA)
  ER bajo  -> mercado lateral      -> reversion (RSI corto en extremos)
Opcion de regimen global con BTC. Solo datos hasta el cierre de cada barra. Formulas publicas; sin codigo de terceros.
"""
import numpy as np
import pandas as pd

from estrategias import ema, rsi, estado, universo, repartir, filtro_btc


def cambio_regimen(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    n = p["n"]
    base = c["BTC"] if (p["global"] and "BTC" in c) else c
    er = (base - base.shift(n)).abs() / base.diff().abs().rolling(n).sum().replace(0, np.nan)
    if p["global"] and "BTC" in c:
        er = pd.DataFrame({k: er for k in cols})
    tendencia = er > p["umbral"]
    e = ema(c, p["ema"])
    sig_t = np.sign(c - e) if p["lados"] == "ambos" else (c > e).astype(float)
    r = rsi(c, p["rsi"])
    larga = estado(r < p["bajo"], r > 50)
    sig_r = larga - estado(r > 100 - p["bajo"], r < 50) if p["lados"] == "ambos" else larga
    s = sig_t.where(tendencia, sig_r).where(er.notna(), 0.0).fillna(0.0)
    return filtro_btc(repartir(s, panel, cols), panel, p)


FAMILIAS = {
    "cambio_regimen": {"fn": cambio_regimen, "fuente": "Regimen por ratio de eficiencia (Kaufman): tendencia vs reversion",
                       "espacio": {"universo": ["grandes", "todas"], "filtro_btc": [0, 1], "lados": ["largo", "ambos"],
                                   "global": [0, 1], "n": [20, 50, 100], "umbral": [0.2, 0.3, 0.4],
                                   "ema": [50, 100, 200], "rsi": [3, 7], "bajo": [20, 30]}},
}
