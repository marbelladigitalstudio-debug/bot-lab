"""
Biblioteca de estrategias. Cada familia = funcion(panel, parametros) -> pesos W (tiempo x moneda).
Solo usan datos HASTA el cierre de cada barra (el motor aplica el desfase).

Fuentes de las ideas (portadas a mano, sin dependencias):
  - freqtrade-strategies-that-work (paulcpk): EMAPriceCrossoverWithThreshold, DoubleEMACrossoverWithTrend,
    MACDCrossoverWithTrend, RSIDirectionalWithTrend(Slow).
  - Clasicos de analisis tecnico: Donchian / tortugas, Bollinger, RSI de reversion.
  - Literatura academica de cripto: momentum de serie temporal (fuerte en largos), momentum de seccion
    cruzada (debil), reversion a corto plazo, funding como senal contraria, baja volatilidad.

Para ANADIR estrategias sin tocar este archivo: crea  lab/extra_loquesea.py  con un diccionario
FAMILIAS = {"nombre": {"fn": funcion, "espacio": {...}, "fuente": "..."}}. Se cargan solas.
"""
import glob
import importlib.util
import os

import numpy as np
import pandas as pd

import comun as C


# ---------------------------------------------------------------- utilidades
def ema(x, n):
    return x.ewm(span=n, adjust=False, min_periods=n).mean()


def rsi(x, n):
    d = x.diff()
    up = d.clip(lower=0).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / n, adjust=False, min_periods=n).mean()
    return 100 - 100 / (1 + up / dn.replace(0, np.nan))


def _ant(b):
    return b.shift(1) if hasattr(b, "shift") else b


def cruza_arriba(a, b):
    return (a > b) & (a.shift(1) <= _ant(b))


def cruza_abajo(a, b):
    return (a < b) & (a.shift(1) >= _ant(b))


def estado(entrada, salida):
    """1 desde una entrada hasta la siguiente salida (maquina de estados vectorizada)."""
    s = pd.DataFrame(np.nan, index=entrada.index, columns=entrada.columns)
    s = s.mask(salida.fillna(False).astype(bool), 0.0)
    s = s.mask(entrada.fillna(False).astype(bool), 1.0)
    return s.ffill().fillna(0.0)


def barras_dia(panel):
    return 24 // (C.MS_INTERVALO[panel["intervalo"]] // C.H)


def universo(panel, p):
    cols = list(panel["close"].columns)
    if p.get("universo") == "grandes":
        cols = [c for c in cols if c in C.GRANDES]
    return cols


def repartir(senal, panel, cols):
    """Senal por moneda (-1/0/1) -> pesos con reparto fijo entre las monedas con precio."""
    cl = panel["close"][cols]
    n = cl.notna().sum(axis=1).replace(0, np.nan)
    return senal[cols].div(n, axis=0).fillna(0.0)


def cada(W, R):
    """Rebalanceo cada R barras: entre medias se mantiene el ultimo peso."""
    if R <= 1:
        return W
    m = np.zeros(len(W), dtype=bool)
    m[::R] = True
    return W.where(pd.Series(m, index=W.index), np.nan).ffill().fillna(0.0)


def filtro_btc(W, panel, p):
    """Si filtro_btc=1: largos solo con BTC por encima de su EMA de 50 dias; cortos solo por debajo."""
    if not p.get("filtro_btc") or "BTC" not in panel["close"]:
        return W
    b = panel["close"]["BTC"]
    sobre = (b > ema(b, 50 * barras_dia(panel))).reindex(W.index).fillna(False)
    largos = W.clip(lower=0).mul(sobre.astype(float), axis=0)
    cortos = W.clip(upper=0).mul((~sobre).astype(float), axis=0)
    return largos + cortos


def dos_lados(ent_l, sal_l, ent_c, sal_c, p):
    largo = estado(ent_l, sal_l)
    if p.get("lados", "largo") == "ambos":
        return largo - estado(ent_c, sal_c)
    return largo


# ---------------------------------------------------------------- familias tecnicas (freqtrade)
def ema_precio_umbral(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    e = ema(c, p["n"])
    u = p["u"]
    s = dos_lados(cruza_arriba(c, e), cruza_abajo(c, e * (1 - u)),
                  cruza_abajo(c, e), cruza_arriba(c, e * (1 + u)), p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def doble_ema_tendencia(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    f, l = ema(c, p["rapida"]), ema(c, p["lenta"])
    if p["tendencia"]:
        t = ema(c, p["tendencia"])
        arriba, abajo = c > t, c < t
    else:
        arriba = abajo = pd.DataFrame(True, index=c.index, columns=c.columns)
    s = dos_lados(cruza_arriba(f, l) & arriba, cruza_abajo(f, l),
                  cruza_abajo(f, l) & abajo, cruza_arriba(f, l), p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def macd_tendencia(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    rap, len_, sen = p["macd"]
    m = ema(c, rap) - ema(c, len_)
    sig = ema(m, sen)
    if p["tendencia"]:
        t = ema(c, p["tendencia"])
        arriba, abajo = c > t, c < t
    else:
        arriba = abajo = pd.DataFrame(True, index=c.index, columns=c.columns)
    s = dos_lados(cruza_arriba(m, sig) & arriba, cruza_abajo(m, sig),
                  cruza_abajo(m, sig) & abajo, cruza_arriba(m, sig), p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def rsi_tendencia(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    lo = panel["low"][cols]
    r = rsi(c, p["n"])
    t = ema(c, p["tendencia"])
    ent = cruza_arriba(r, p["entrada"]) & (lo > t)
    sal = cruza_abajo(r, p["salida"]) | (lo < t)
    s = estado(ent, sal)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def donchian(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    hi = panel["high"][cols].rolling(p["n"]).max().shift(1)
    lo = panel["low"][cols].rolling(p["n"]).min().shift(1)
    hi_s = panel["high"][cols].rolling(p["m"]).max().shift(1)
    lo_s = panel["low"][cols].rolling(p["m"]).min().shift(1)
    s = dos_lados(c > hi, c < lo_s, c < lo, c > hi_s, p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


# ---------------------------------------------------------------- reversion
def bollinger_reversion(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    m = c.rolling(p["n"]).mean()
    sd = c.rolling(p["n"]).std()
    z = (c - m) / sd
    if p["filtro"]:
        t = ema(c, p["filtro"])
        ok_l, ok_c = c > t, c < t
    else:
        ok_l = ok_c = pd.DataFrame(True, index=c.index, columns=c.columns)
    s = dos_lados((z < -p["k"]) & ok_l, z > -p["salida"],
                  (z > p["k"]) & ok_c, z < p["salida"], p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


def rsi_reversion(panel, p):
    cols = universo(panel, p)
    c = panel["close"][cols]
    r = rsi(c, p["n"])
    if p["filtro"]:
        t = ema(c, p["filtro"])
        ok_l, ok_c = c > t, c < t
    else:
        ok_l = ok_c = pd.DataFrame(True, index=c.index, columns=c.columns)
    s = dos_lados((r < p["bajo"]) & ok_l, r > p["sale"],
                  (r > 100 - p["bajo"]) & ok_c, r < 100 - p["sale"], p)
    return filtro_btc(repartir(s, panel, cols), panel, p)


# ---------------------------------------------------------------- momentum / factores
def _vol(panel, cols, dias):
    r = panel["close"][cols].pct_change(fill_method=None)
    return r.rolling(max(5, int(dias * barras_dia(panel)))).std()


def ts_momentum(panel, p):
    cols = universo(panel, p)
    bd = barras_dia(panel)
    c = panel["close"][cols]
    ret = c / c.shift(int(p["dias"] * bd)) - 1
    s = (ret > 0).astype(float)
    if p["lados"] == "ambos":
        s = s - (ret < 0).astype(float)
    s = s.where(ret.notna(), 0.0)
    if p["vol"]:
        iv = 1 / _vol(panel, cols, 30).replace(0, np.nan)
        peso = iv.div(iv.sum(axis=1), axis=0)
        W = (s * peso).fillna(0.0)
    else:
        W = repartir(s, panel, cols)
    return filtro_btc(cada(W, int(p["mantener"] * bd)), panel, p)


def _seccion(panel, p, puntuacion, cols):
    """Largos en el q superior de 'puntuacion', cortos en el inferior (o solo largos)."""
    rk = puntuacion.rank(axis=1, pct=True)
    n = puntuacion.notna().sum(axis=1)
    valido = n >= 5
    arriba = (rk > 1 - p["q"]) & valido.values[:, None]
    abajo = (rk <= p["q"]) & valido.values[:, None]
    na = arriba.sum(axis=1).replace(0, np.nan)
    nb = abajo.sum(axis=1).replace(0, np.nan)
    if p["modo"] == "largo":
        W = arriba.astype(float).div(na, axis=0)
    else:
        W = arriba.astype(float).div(na, axis=0) * 0.5 - abajo.astype(float).div(nb, axis=0) * 0.5
    return W.fillna(0.0)


def xs_momentum(panel, p):
    cols = universo(panel, p)
    bd = barras_dia(panel)
    c = panel["close"][cols]
    punt = c / c.shift(int(p["dias"] * bd)) - 1
    W = _seccion(panel, p, punt, cols)
    return filtro_btc(cada(W, int(p["mantener"] * bd)), panel, p)


def xs_reversion(panel, p):
    cols = universo(panel, p)
    bd = barras_dia(panel)
    c = panel["close"][cols]
    k = max(1, int(round(p["dias"] * bd)))
    punt = -(c / c.shift(k) - 1)
    W = _seccion(panel, p, punt, cols)
    return filtro_btc(cada(W, max(1, int(round(p["mantener"] * bd)))), panel, p)


def funding_contrario(panel, p):
    """Largo donde el funding medio reciente es mas negativo (cortos apinados), corto donde es mas alto."""
    cols = universo(panel, p)
    bd = barras_dia(panel)
    f = panel["funding"][cols].rolling(int(p["dias"] * bd)).mean()
    f = f.where(panel["close"][cols].notna())
    W = _seccion(panel, p, -f, cols)
    return filtro_btc(cada(W, int(p["mantener"] * bd)), panel, p)


def baja_volatilidad(panel, p):
    cols = universo(panel, p)
    bd = barras_dia(panel)
    v = _vol(panel, cols, p["dias"])
    W = _seccion(panel, dict(p, modo="largo"), -v, cols)
    if p["modo"] == "cubierto_btc" and "BTC" in panel["close"]:
        W = W * 0.5
        W["BTC"] = W.get("BTC", 0.0) - 0.5 * (W.sum(axis=1) > 0)
    return filtro_btc(cada(W, int(p["mantener"] * bd)), panel, p)


# ---------------------------------------------------------------- registro
U = {"universo": ["grandes", "todas"], "filtro_btc": [0, 1]}
FAMILIAS = {
    "ema_precio_umbral": {"fn": ema_precio_umbral, "fuente": "freqtrade EMAPriceCrossoverWithThreshold",
                          "espacio": dict(U, n=[50, 100, 200, 400, 800], u=[0.0, 0.01, 0.03], lados=["largo", "ambos"])},
    "doble_ema_tendencia": {"fn": doble_ema_tendencia, "fuente": "freqtrade DoubleEMACrossoverWithTrend",
                            "espacio": dict(U, rapida=[9, 12, 21], lenta=[26, 50, 100], tendencia=[0, 200, 400],
                                            lados=["largo", "ambos"])},
    "macd_tendencia": {"fn": macd_tendencia, "fuente": "freqtrade MACDCrossoverWithTrend",
                       "espacio": dict(U, macd=[(12, 26, 9), (8, 21, 5), (24, 52, 18)], tendencia=[0, 200, 400],
                                       lados=["largo", "ambos"])},
    "rsi_tendencia": {"fn": rsi_tendencia, "fuente": "freqtrade RSIDirectionalWithTrend(Slow)",
                      "espacio": dict(U, n=[7, 10, 14], entrada=[25, 30, 35], salida=[15, 20, 25],
                                      tendencia=[200, 400, 600])},
    "donchian": {"fn": donchian, "fuente": "Tortugas / canal de Donchian",
                 "espacio": dict(U, n=[20, 55, 100, 200], m=[10, 20, 50], lados=["largo", "ambos"])},
    "bollinger_reversion": {"fn": bollinger_reversion, "fuente": "Bandas de Bollinger (reversion)",
                            "espacio": dict(U, n=[20, 50, 100], k=[1.5, 2.0, 2.5, 3.0], salida=[0.0, 0.5],
                                            filtro=[0, 400], lados=["largo", "ambos"])},
    "rsi_reversion": {"fn": rsi_reversion, "fuente": "RSI de reversion (Connors)",
                      "espacio": dict(U, n=[2, 4, 7, 14], bajo=[10, 20, 30], sale=[50, 60, 70],
                                      filtro=[0, 400], lados=["largo", "ambos"])},
    "ts_momentum": {"fn": ts_momentum, "fuente": "Momentum de serie temporal (Liu-Tsyvinski; AUT 2024)",
                    "espacio": dict(U, dias=[3, 7, 14, 28, 56], mantener=[1, 3, 5, 7], lados=["largo", "ambos"],
                                    vol=[0, 1])},
    "xs_momentum": {"fn": xs_momentum, "fuente": "Momentum de seccion cruzada",
                    "espacio": dict(U, dias=[1, 3, 7, 14, 28], mantener=[1, 3, 7], q=[0.2, 0.33],
                                    modo=["ls", "largo"])},
    "xs_reversion": {"fn": xs_reversion, "fuente": "Reversion a corto plazo (seccion cruzada)",
                     "espacio": dict(U, dias=[0.25, 0.5, 1, 2, 3], mantener=[0.25, 0.5, 1, 2], q=[0.2, 0.33],
                                     modo=["ls", "largo"])},
    "funding_contrario": {"fn": funding_contrario, "fuente": "Funding extremo como senal contraria",
                          "espacio": dict(U, dias=[1, 3, 7, 14], mantener=[1, 3, 7], q=[0.2, 0.33],
                                          modo=["ls", "largo"])},
    "baja_volatilidad": {"fn": baja_volatilidad, "fuente": "Anomalia de baja volatilidad",
                         "espacio": dict(U, dias=[7, 14, 30], mantener=[1, 7], q=[0.2, 0.33],
                                         modo=["largo", "cubierto_btc"])},
}


def _cargar_extras():
    for ruta in sorted(glob.glob(os.path.join(C.CARPETA, "extra_*.py"))):
        try:
            spec = importlib.util.spec_from_file_location(os.path.basename(ruta)[:-3], ruta)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            for k, v in getattr(mod, "FAMILIAS", {}).items():
                FAMILIAS[k] = v
                print(f"  (familia extra cargada: {k} desde {os.path.basename(ruta)})")
        except Exception as e:
            print(f"  AVISO: no pude cargar {ruta}: {e}")


_cargar_extras()


def tamano_espacio(fam):
    n = 1
    for v in FAMILIAS[fam]["espacio"].values():
        n *= len(v)
    return n


def clave(fam, p):
    return fam + "|" + "|".join(f"{k}={p[k]}" for k in sorted(p))


def vecinos(fam, p):
    """Parametros a un paso en cada eje (para medir estabilidad)."""
    esp = FAMILIAS[fam]["espacio"]
    out = []
    for k, vals in esp.items():
        if len(vals) < 2 or k in ("universo", "lados", "modo", "filtro_btc"):
            continue
        i = vals.index(p[k])
        for j in (i - 1, i + 1):
            if 0 <= j < len(vals):
                out.append(dict(p, **{k: vals[j]}))
    return out
