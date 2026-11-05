"""
Familias extra reescritas desde formulas publicas de analisis tecnico (NO se ha copiado codigo).
Ideas vistas en freqtrade-strategies (GPL-3.0, f3340ce) y literatura clasica; ver referencias/MANIFIESTO.md.
Aviso: la cache solo trae apertura y maximo, asi que el minimo es aproximado (min(apertura, cierre));
por eso el rango verdadero es solo orientativo. Todo usa datos hasta el cierre de cada barra.
"""
import numpy as np
import pandas as pd

import estrategias as E
from estrategias import ema, estado, universo, repartir, filtro_btc, dos_lados, cruza_arriba, cruza_abajo, barras_dia


def _atr(panel, cols, n):
    c, h, l = panel["close"][cols], panel["high"][cols], panel["low"][cols]
    pc = c.shift(1)
    tr = np.maximum(h - l, np.maximum((h - pc).abs(), (l - pc).abs()))
    return tr.ewm(alpha=1 / n, adjust=False, min_periods=n).mean()


def supertrend(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    atr = _atr(panel, cols, p["n"])
    mid = (panel["high"][cols] + panel["low"][cols]) / 2
    sup, inf = mid + p["k"] * atr, mid - p["k"] * atr
    a = c.values
    S, I = sup.values.copy(), inf.values.copy()
    dirn = np.zeros_like(a)
    fs, fi = S.copy(), I.copy()
    for t in range(1, len(a)):
        # bandas finales: solo se acercan al precio (formula clasica)
        fs[t] = np.where((S[t] < fs[t - 1]) | (a[t - 1] > fs[t - 1]), S[t], fs[t - 1])
        fi[t] = np.where((I[t] > fi[t - 1]) | (a[t - 1] < fi[t - 1]), I[t], fi[t - 1])
        d = dirn[t - 1]
        d = np.where(a[t] > fs[t - 1], 1.0, np.where(a[t] < fi[t - 1], -1.0, d))
        dirn[t] = np.where(np.isnan(fs[t]) | np.isnan(fi[t]), 0.0, d)
    d = pd.DataFrame(dirn, index=c.index, columns=cols)
    s = d if p["lados"] == "ambos" else d.clip(lower=0)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def keltner_ruptura(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    e, atr = ema(c, p["n"]), _atr(panel, cols, p["n"])
    sup, inf = e + p["k"] * atr, e - p["k"] * atr
    s = dos_lados(c > sup, c < e, c < inf, c > e, p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def ichimoku_cierre(panel, p):
    """Version con cierres: tenkan/kijun = medio del canal; nube = media de ambos (sin desplazar al futuro)."""
    cols = universo(panel, p)
    c = panel["close"][cols]
    mid = lambda n: (c.rolling(n).max() + c.rolling(n).min()) / 2
    ten, kij = mid(p["t"]), mid(p["k"])
    nube_a = (ten + kij) / 2
    nube_b = mid(p["s"])
    techo, suelo = np.maximum(nube_a, nube_b), np.minimum(nube_a, nube_b)
    s = dos_lados((c > techo) & (ten > kij), c < kij,
                  (c < suelo) & (ten < kij), c > kij, p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def kama_tendencia(panel, p):
    """Media adaptativa de Kaufman: sigue la tendencia cuando el ratio de eficiencia es alto."""
    cols = universo(panel, p)
    c = panel["close"][cols]
    n = p["n"]
    er = (c - c.shift(n)).abs() / c.diff().abs().rolling(n).sum().replace(0, np.nan)
    f, l = 2 / (p["rapida"] + 1), 2 / (p["lenta"] + 1)
    sc = ((er * (f - l) + l) ** 2).values
    a = c.values
    k = np.full_like(a, np.nan)
    for t in range(len(a)):
        prev = k[t - 1] if t else np.full(a.shape[1], np.nan)
        ini = np.isnan(prev) & ~np.isnan(sc[t])
        nxt = prev + sc[t] * (a[t] - prev)
        k[t] = np.where(ini, a[t], nxt)
    k = pd.DataFrame(k, index=c.index, columns=cols)
    s = dos_lados(cruza_arriba(c, k) | ((c > k) & (er > p["er_min"])), c < k,
                  cruza_abajo(c, k) | ((c < k) & (er > p["er_min"])), c > k, p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def squeeze_ruptura(panel, p):
    """Bandas de Bollinger muy estrechas (percentil bajo de su ancho) seguidas de ruptura."""
    cols = universo(panel, p)
    c = panel["close"][cols]
    m, sd = c.rolling(p["n"]).mean(), c.rolling(p["n"]).std()
    ancho = (4 * sd / m)
    bd = barras_dia(panel)
    ventana = int(30 * bd)
    comprimido = ancho.rolling(5).min() <= ancho.rolling(ventana, min_periods=ventana // 2).quantile(p["pct"])
    ent_l = (c > m + 2 * sd) & comprimido.shift(1).fillna(False)
    ent_c = (c < m - 2 * sd) & comprimido.shift(1).fillna(False)
    s = dos_lados(ent_l, c < m, ent_c, c > m, p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


U = {"universo": ["grandes", "todas"], "filtro_btc": [0, 1], "lados": ["largo", "ambos"]}
FAMILIAS = {
    "supertrend": {"fn": supertrend, "fuente": "Supertrend (freqtrade-strategies, GPL; reescrito de la formula ATR)",
                   "espacio": dict(U, n=[10, 14, 30, 60], k=[2.0, 3.0, 4.0, 6.0])},
    "keltner_ruptura": {"fn": keltner_ruptura, "fuente": "Canal de Keltner (formula publica)",
                        "espacio": dict(U, n=[20, 50, 100], k=[1.5, 2.0, 3.0])},
    "ichimoku_cierre": {"fn": ichimoku_cierre, "fuente": "Ichimoku adaptado a cierres (formula publica)",
                        "espacio": dict(U, t=[9, 20, 40], k=[26, 52, 104], s=[52, 104, 208])},
    "kama_tendencia": {"fn": kama_tendencia, "fuente": "KAMA de Kaufman (formula publica)",
                       "espacio": dict(U, n=[10, 20, 40], rapida=[2, 5], lenta=[30, 60], er_min=[0.2, 0.35])},
    "squeeze_ruptura": {"fn": squeeze_ruptura, "fuente": "Squeeze de Bollinger (formula publica)",
                        "espacio": dict(U, n=[20, 50], pct=[0.1, 0.2])},
}
