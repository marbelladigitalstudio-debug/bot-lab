"""
S&P 500 y ETFs (diario) con yfinance (Apache-2.0). Datos publicos de Yahoo; sin claves.
Guarda lab/datos/acciones_1d.pkl.gz como panel {open, high, low, close, volume, funding=0, intervalo='1d'}.
Uso:  python -m herramientas.descarga_acciones --desde 2005-01-01
Nota: en acciones el ano tiene ~252 sesiones (en cripto 365): usar BARRAS_ANO_ACCIONES para anualizar.
"""
import argparse

import numpy as np
import pandas as pd

from herramientas import requiere
import datos as D

TICKERS = ["SPY", "QQQ", "IWM", "DIA", "TLT", "GLD", "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLU", "XLB",
           "^GSPC", "^VIX"]
BARRAS_ANO_ACCIONES = 252


def descargar(tickers, desde):
    yf = requiere("yfinance", "datos.txt")
    df = yf.download(tickers, start=desde, interval="1d", auto_adjust=True, progress=False, group_by="column")
    panel = {}
    for campo, k in (("Open", "open"), ("High", "high"), ("Low", "low"), ("Close", "close"), ("Volume", "volume")):
        x = df[campo].copy()
        x.index = (pd.DatetimeIndex(x.index).tz_localize(None).astype("int64") // 10**6).astype("int64")
        panel[k] = x
    panel["funding"] = pd.DataFrame(0.0, index=panel["close"].index, columns=panel["close"].columns)
    panel["intervalo"] = "1d"
    panel["aproximado"] = False
    return panel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", default="2005-01-01")
    ap.add_argument("--tickers", nargs="+", default=TICKERS)
    a = ap.parse_args()
    p = descargar(a.tickers, a.desde)
    D._escribir("acciones_1d.pkl.gz", p)
    print(f"Guardado lab/datos/acciones_1d.pkl.gz: {p['close'].shape[0]} sesiones x {p['close'].shape[1]} tickers")


def cargar():
    return D._leer("acciones_1d.pkl.gz", None)


if __name__ == "__main__":
    main()
