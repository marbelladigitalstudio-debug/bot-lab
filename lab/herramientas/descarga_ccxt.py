"""
Historia LARGA de cripto desde exchanges publicos con ccxt (MIT). Sin claves: solo endpoints publicos.
Escribe lab/datos/base_<exchange>.pkl.gz con el MISMO formato que datos.py, asi el laboratorio lo usa con:
    set LAB_BASE=base_binanceusdm.pkl.gz   (Windows)   /   export LAB_BASE=...  (Linux/Mac)
Uso:  python -m herramientas.descarga_ccxt --exchange binanceusdm --desde 2022-01-01 --intervalos 1h 4h
Por defecto baja perpetuos USDT de las monedas grandes (incluye funding).
"""
import argparse
import time

from herramientas import requiere
import comun as C
import datos as D

MONEDAS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "ADA", "LINK", "AVAX", "LTC", "DOT", "TRX", "BCH", "NEAR",
           "SUI", "APT", "ARB", "OP", "INJ", "AAVE"]


def _simbolo(ex, moneda):
    for s in (f"{moneda}/USDT:USDT", f"{moneda}/USDT", f"{moneda}/USD:USD"):
        if s in ex.markets:
            return s
    return None


def velas(ex, simbolo, iv, desde_ms, hasta_ms):
    out, t = {}, desde_ms
    paso = C.MS_INTERVALO[iv]
    while t < hasta_ms:
        lote = ex.fetch_ohlcv(simbolo, iv, since=t, limit=1000)
        if not lote:
            break
        antes = len(out)
        for ts, o, h, l, c, v in lote:
            out[int(ts)] = (float(o), float(h), float(l), float(c), float(v or 0))
        if len(out) == antes:          # la pagina no trae nada nuevo: fin
            break
        nuevo = int(lote[-1][0]) + paso
        if nuevo <= t:
            break
        t = nuevo
    return out


def funding(ex, simbolo, desde_ms, hasta_ms):
    if not ex.has.get("fetchFundingRateHistory"):
        return {}
    out, t = {}, desde_ms
    while t < hasta_ms:
        lote = ex.fetch_funding_rate_history(simbolo, since=t, limit=1000)
        if not lote:
            break
        antes = len(out)
        for x in lote:
            out[int(x["timestamp"]) // C.H * C.H] = float(x["fundingRate"])
        if len(out) == antes:
            break
        nuevo = int(lote[-1]["timestamp"]) + 1
        if nuevo <= t:
            break
        t = nuevo
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exchange", default="binanceusdm")
    ap.add_argument("--desde", default="2022-01-01")
    ap.add_argument("--intervalos", nargs="+", default=["1h", "4h"])
    ap.add_argument("--monedas", nargs="+", default=MONEDAS)
    a = ap.parse_args()
    ccxt = requiere("ccxt", "datos.txt")
    ex = getattr(ccxt, a.exchange)({"enableRateLimit": True})   # sin apiKey: solo datos publicos
    ex.load_markets()
    nombre = f"base_{a.exchange}.pkl.gz"
    base = D._leer(nombre, {"velas": {}, "funding": {}, "fuente": a.exchange})
    ahora = int(time.time() * 1000)
    desde = int(ex.parse8601(a.desde + "T00:00:00Z"))
    for i, m in enumerate(a.monedas, 1):
        s = _simbolo(ex, m)
        if not s:
            print(f"  {m}: no esta en {a.exchange}")
            continue
        print(f"  [{i}/{len(a.monedas)}] {m} ({s})")
        for iv in a.intervalos:
            v = base["velas"].setdefault(iv, {}).setdefault(m, {})
            ini = max(v) - 2 * C.MS_INTERVALO[iv] if v else desde
            v.update(velas(ex, s, iv, ini, ahora))
        f = base["funding"].setdefault(m, {})
        f.update(funding(ex, s, max(f) if f else desde, ahora))
        D._escribir(nombre, base)
    base["actualizado"] = ahora
    D._escribir(nombre, base)
    print(f"Guardado en lab/datos/{nombre}. Para usarlo: LAB_BASE={nombre}")


if __name__ == "__main__":
    main()
