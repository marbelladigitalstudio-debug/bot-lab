"""
Datos del laboratorio: velas OHLCV y funding de Hyperliquid (API publica, gratis).

  python datos.py            -> descarga / actualiza 1h y 4h
La primera vez tarda (~1 hora: la API limita el ritmo). Despues solo baja lo nuevo (1-3 min).
Cada dia se ACUMULA historia: Hyperliquid solo sirve las ultimas 5000 velas,
pero lo que ya esta guardado no se borra, asi que la base crece con el tiempo.
"""
import gzip
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

import comun as C


def _ruta(nombre):
    return os.path.join(C.CARPETA_DATOS, nombre)


def _leer(nombre, defecto):
    try:
        with gzip.open(_ruta(nombre), "rb") as f:
            return pickle.load(f)
    except (OSError, EOFError, pickle.UnpicklingError):
        return defecto


def _escribir(nombre, obj):
    tmp = _ruta(nombre) + ".tmp"
    with gzip.open(tmp, "wb") as f:
        pickle.dump(obj, f)
    os.replace(tmp, _ruta(nombre))


def monedas_top(n):
    meta, ctxs = C.info({"type": "metaAndAssetCtxs"})
    lista = []
    for m, c in zip(meta["universe"], ctxs):
        if m.get("isDelisted"):
            continue
        lista.append((float(c.get("dayNtlVlm") or 0), m["name"]))
    return [nm for _, nm in sorted(lista, reverse=True)[:n]]


def _bajar_velas(moneda, iv, desde, hasta):
    paso = C.MS_INTERVALO[iv]
    filas, t = {}, desde
    while t < hasta:
        r = C.info({"type": "candleSnapshot",
                    "req": {"coin": moneda, "interval": iv, "startTime": int(t), "endTime": int(hasta)}})
        if not r:
            break
        for x in r:
            filas[int(x["t"])] = (float(x["o"]), float(x["h"]), float(x["l"]), float(x["c"]), float(x["v"]))
        nuevo = max(int(x["t"]) for x in r) + paso
        if nuevo <= t or len(r) < 4900:
            break
        t = nuevo
    return filas


def _bajar_funding(moneda, desde, hasta):
    filas, t = {}, desde
    while t < hasta:
        r = C.info({"type": "fundingHistory", "coin": moneda, "startTime": int(t), "endTime": int(hasta)})
        if not r:
            break
        for x in r:
            filas[int(x["time"]) // C.H * C.H] = float(x["fundingRate"])
        nuevo = int(r[-1]["time"]) + 1
        if nuevo <= t or len(r) < 500:
            break
        t = nuevo
    return filas


def actualizar(intervalos=("1h", "4h"), top=C.TOP_MONEDAS):
    ahora = int(time.time() * 1000)
    print("Buscando las monedas con mas volumen...")
    nuevas = monedas_top(top)
    base = _leer("base.pkl.gz", {"velas": {}, "funding": {}})
    monedas = sorted(set(nuevas) | set(base["funding"]))   # nunca se olvida una moneda guardada
    for iv in intervalos:
        base["velas"].setdefault(iv, {})
    for i, c in enumerate(monedas, 1):
        print(f"  [{i}/{len(monedas)}] {c}")
        for iv in intervalos:
            v = base["velas"][iv].setdefault(c, {})
            paso = C.MS_INTERVALO[iv]
            desde = (max(v) - 2 * paso) if v else ahora - 5000 * paso
            try:
                v.update(_bajar_velas(c, iv, desde, ahora))
            except Exception as e:
                print(f"     velas {iv}: fallo ({e}); sigo")
        f = base["funding"].setdefault(c, {})
        desde = (max(f) - 2 * C.H) if f else ahora - 5000 * C.MS_INTERVALO[intervalos[-1]]
        try:
            f.update(_bajar_funding(c, desde, ahora))
        except Exception as e:
            print(f"     funding: fallo ({e}); sigo")
        if i % 5 == 0:
            _escribir("base.pkl.gz", base)
    base["actualizado"] = ahora
    _escribir("base.pkl.gz", base)
    print("Datos guardados en lab\\datos\\base.pkl.gz")


def _panel_desde_base(base, iv):
    paso = C.MS_INTERVALO[iv]
    velas = base["velas"].get(iv, {})
    campos = {"open": 0, "high": 1, "low": 2, "close": 3, "volume": 4}
    out = {}
    for nombre, k in campos.items():
        out[nombre] = pd.DataFrame({c: pd.Series({t: x[k] for t, x in v.items()}) for c, v in velas.items() if v})
    idx = out["close"].index.sort_values()
    # la ultima vela puede estar a medias: se descarta
    ahora = base.get("actualizado", int(time.time() * 1000))
    idx = idx[idx + paso <= ahora]
    for k in out:
        out[k] = out[k].reindex(idx)
    out["funding"] = _funding_por_barra(base["funding"], idx, paso, list(out["close"].columns))
    out["intervalo"] = iv
    out["aproximado"] = False
    return out


def _funding_por_barra(funding, idx, paso, monedas):
    """Funding pagado mientras se mantiene la posicion desde el cierre de la barra anterior
    hasta el cierre de esta (horas dentro de (t, t+paso])."""
    res = {}
    for c in monedas:
        f = funding.get(c, {})
        if not f:
            res[c] = pd.Series(0.0, index=idx)
            continue
        s = pd.Series(f).sort_index()
        barra = ((s.index - 1) // paso) * paso       # hora h pertenece a la barra que termina en h
        res[c] = s.groupby(barra).sum().reindex(idx).fillna(0.0)
    return pd.DataFrame(res, index=idx)


def desde_cache_antigua(ruta, iv="1h"):
    """Convierte cache_funding.pkl.gz (velas 1h con solo apertura y maximo) en un panel.
    cierre(t) = apertura(t+1). Sin minimo ni volumen: marcado como aproximado."""
    with gzip.open(ruta, "rb") as f:
        d = pickle.load(f)
    H = C.H
    o = pd.DataFrame({c: pd.Series({t * H: x[0] for t, x in v.items()}) for c, v in d["velas"].items() if v})
    h = pd.DataFrame({c: pd.Series({t * H: x[1] for t, x in v.items()}) for c, v in d["velas"].items() if v})
    o = o.sort_index()
    h = h.reindex(o.index)
    cl = o.shift(-1)
    o, h, cl = o.iloc[:-1], h.iloc[:-1], cl.iloc[:-1]
    lo = np.minimum(o, cl)
    fund = {c: {t * H: r for t, r in v.items()} for c, v in d["funding"].items()}
    panel = {"open": o, "high": np.maximum(h, cl), "low": lo, "close": cl,
             "volume": pd.DataFrame(np.nan, index=o.index, columns=o.columns)}
    panel["funding"] = _funding_por_barra(fund, o.index, H, list(o.columns))
    panel["intervalo"] = "1h"
    panel["aproximado"] = True
    if iv != "1h":
        panel = remuestrear(panel, iv)
    return panel


def remuestrear(panel, iv):
    paso = C.MS_INTERVALO[iv]
    g = (panel["close"].index // paso) * paso
    out = {"open": panel["open"].groupby(g).first(), "high": panel["high"].groupby(g).max(),
           "low": panel["low"].groupby(g).min(), "close": panel["close"].groupby(g).last(),
           "volume": panel["volume"].groupby(g).sum(min_count=1),
           "funding": panel["funding"].groupby(g).sum()}
    n = panel["close"].groupby(g).count()
    completo = n.max(axis=1) == paso // C.H
    for k in list(out):
        out[k] = out[k][completo]
    out["intervalo"] = iv
    out["aproximado"] = panel.get("aproximado", False)
    return out


def cargar(iv):
    """Panel listo para el motor. Usa la base descargada; si no existe, la cache antigua."""
    base = _leer("base.pkl.gz", None)
    if base and base["velas"].get(iv):
        return _panel_desde_base(base, iv)
    antigua = os.path.join(os.path.dirname(C.CARPETA), "cache_funding.pkl.gz")
    if os.path.exists(antigua):
        print("AVISO: sin datos propios del laboratorio; uso cache_funding.pkl.gz (aproximada, 180 dias).")
        return desde_cache_antigua(antigua, iv)
    raise SystemExit("No hay datos. Ejecuta primero: python datos.py")


if __name__ == "__main__":
    ivs = tuple(sys.argv[1:]) or ("1h", "4h")
    actualizar(ivs)
