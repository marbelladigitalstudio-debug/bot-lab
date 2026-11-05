"""
Motor de backtest vectorizado.

Convencion SIN mirar el futuro:
  W[t] = pesos decididos con datos hasta el CIERRE de la barra t.
  Se ejecutan al cierre de t y ganan/pierden lo que pase en la barra t+1:
      pnl[t+1] = sum_i W[t,i] * r[t+1,i]  -  coste * |W[t] - W[t-1]|  -  W[t,i] * funding[t+1,i]
  (los largos pagan el funding positivo; los cortos lo cobran)
Los pesos se limitan a exposicion bruta <= 1 (sin apalancamiento).
"""
import numpy as np
import pandas as pd

import comun as C


def limpiar_pesos(W, panel):
    W = W.reindex_like(panel["close"]).fillna(0.0)
    W = W.where(panel["close"].notna(), 0.0)              # no se opera una moneda sin precio
    bruto = W.abs().sum(axis=1)
    escala = np.where(bruto > 1.0, 1.0 / bruto.replace(0, 1), 1.0)
    return W.mul(escala, axis=0)


def simular(W, panel, coste_lado=C.COSTE_LADO):
    """Devuelve dict con la serie de rentabilidad por barra y detalles."""
    W = limpiar_pesos(W, panel)
    r = panel["close"].pct_change(fill_method=None).fillna(0.0)
    Wp = W.shift(1).fillna(0.0)                         # posicion mantenida durante la barra
    bruto = (Wp * r).sum(axis=1)
    fund = (Wp * panel["funding"].reindex_like(W).fillna(0.0)).sum(axis=1)
    giro = (W - W.shift(1).fillna(0.0)).abs()
    coste = giro.sum(axis=1).shift(1).fillna(0.0) * coste_lado  # coste al ejecutar (cuenta en la barra siguiente)
    neto = bruto - fund - coste
    por_moneda = (Wp * r).sum(axis=0) - (Wp * panel["funding"].reindex_like(W).fillna(0.0)).sum(axis=0) \
        - giro.sum(axis=0) * coste_lado
    return {"ret": neto, "bruto": bruto, "funding": fund, "coste": coste,
            "giro": giro.sum(axis=1), "exposicion": W.abs().sum(axis=1),
            "por_moneda": por_moneda, "W": W}


def metricas(ret, iv, giro=None, exposicion=None):
    ret = ret.dropna()
    n = len(ret)
    if n < 10:
        return {"n": n, "sharpe": 0.0, "sr_barra": 0.0, "anual": 0.0, "max_caida": 0.0,
                "asim": 0.0, "curt": 3.0, "operaciones": 0, "exposicion": 0.0}
    ba = C.BARRAS_ANO[iv]
    m, s = ret.mean(), ret.std(ddof=1)
    sr = m / s if s > 0 else 0.0
    eq = (1 + ret).cumprod()
    caida = (eq / eq.cummax() - 1).min()
    z = (ret - m) / s if s > 0 else ret * 0
    asim = float((z ** 3).mean()) if s > 0 else 0.0
    curt = float((z ** 4).mean()) if s > 0 else 3.0
    ops = int((giro > 1e-9).sum()) if giro is not None else 0
    return {"n": n, "sharpe": float(sr * np.sqrt(ba)), "sr_barra": float(sr),
            "anual": float(m * ba), "max_caida": float(caida), "asim": asim, "curt": curt,
            "operaciones": ops,
            "exposicion": float(exposicion.mean()) if exposicion is not None else 0.0}


def por_meses(ret, iv):
    ms = C.MS_INTERVALO[iv]
    mes = pd.to_datetime(ret.index, unit="ms").to_period("M")
    return ret.groupby(mes).sum()
