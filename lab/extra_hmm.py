"""
Regimen por HMM (hmmlearn, BSD) sobre BTC: la "inteligencia" que decide QUE estrategia usar.
  regimen tranquilo -> seguir tendencia (precio > EMA);  regimen agitado -> fuera del mercado o reversion RSI.
El HMM se re-entrena hacia delante con SOLO el pasado (herramientas/regimen.py; test de truncado superado).
Si hmmlearn no esta instalado, esta familia no se registra (el laboratorio sigue funcionando igual).
"""
import numpy as np
import pandas as pd

from estrategias import ema, rsi, estado, universo, repartir, filtro_btc, barras_dia

try:
    from herramientas import regimen as R
    import hmmlearn  # noqa: F401
    DISPONIBLE = True
except Exception:
    DISPONIBLE = False

_CACHE = {}


def _p_agitado(panel, cada):
    precio = panel["close"]["BTC"].dropna()
    k = (panel["intervalo"], int(precio.index[0]), int(precio.index[-1]), len(precio), cada)
    if k not in _CACHE:
        minimo = 60 * barras_dia(panel)     # fijo (60 dias): NO puede depender de la longitud total
        _CACHE[k] = R.hmm_regimen(precio, minimo=minimo, cada=cada)
    return _CACHE[k].reindex(panel["close"].index)


def hmm_regimen(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    agit = _p_agitado(panel, p["cada"])
    tranquilo = (agit < p["umbral"]).reindex(c.index).fillna(False)
    tend = (c > ema(c, p["ema"])).astype(float)
    if p["agitado"] == "reversion":
        r = rsi(c, 3)
        alt = estado(r < 20, r > 50)
    else:
        alt = tend * 0.0
    s = tend.where(tranquilo.values[:, None].repeat(len(cols), 1), alt)
    s = s.where(agit.notna().values[:, None].repeat(len(cols), 1), 0.0)
    return filtro_btc(repartir(s, panel, cols), panel, p)


FAMILIAS = {}
if DISPONIBLE:
    FAMILIAS["hmm_regimen"] = {"fn": hmm_regimen, "fuente": "HMM gaussiano de 2 estados sobre BTC (hmmlearn); tendencia solo en calma",
                               "espacio": {"universo": ["grandes", "todas"], "filtro_btc": [0, 1], "cada": [100, 200],
                                           "umbral": [0.3, 0.5, 0.7], "ema": [50, 100, 200],
                                           "agitado": ["fuera", "reversion"]}}
