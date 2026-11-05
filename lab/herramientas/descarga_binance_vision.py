"""
Historia larga desde el archivo PUBLICO de Binance (data.binance.vision): ficheros mensuales de velas y funding
de futuros USDT-M. Sin claves, sin API (son ficheros estaticos), y normalmente accesible desde cualquier pais.
Escribe lab/datos/base_binancevision.pkl.gz con el mismo formato que datos.py  ->  LAB_BASE=base_binancevision.pkl.gz
Uso:  python -m herramientas.descarga_binance_vision --desde 2022-01
"""
import argparse
import csv
import io
import time
import zipfile

import pandas as pd
import requests

import herramientas  # noqa: F401  (anade lab/ a sys.path)
import comun as C
import datos as D
from herramientas.descarga_ccxt import MONEDAS

URL = "https://data.binance.vision/data/futures/um/monthly"


def _filas_csv(contenido):
    with zipfile.ZipFile(io.BytesIO(contenido)) as z:
        with z.open(z.namelist()[0]) as f:
            for fila in csv.reader(io.TextIOWrapper(f, encoding="utf-8")):
                if fila and fila[0][:1].isdigit():      # salta la cabecera si la hay
                    yield fila


def velas_mes(sesion, simbolo, iv, mes):
    r = sesion.get(f"{URL}/klines/{simbolo}/{iv}/{simbolo}-{iv}-{mes}.zip", timeout=60)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    out = {}
    for f in _filas_csv(r.content):
        t = int(f[0])
        t = t // 1000 if t > 10**14 else t                  # algunos ficheros recientes vienen en microsegundos
        out[t] = (float(f[1]), float(f[2]), float(f[3]), float(f[4]), float(f[5]))
    return out


def funding_mes(sesion, simbolo, mes):
    r = sesion.get(f"{URL}/fundingRate/{simbolo}/{simbolo}-fundingRate-{mes}.zip", timeout=60)
    if r.status_code == 404:
        return {}
    r.raise_for_status()
    out = {}
    for f in _filas_csv(r.content):
        t = int(f[0])
        t = t // 1000 if t > 10**14 else t
        out[t // C.H * C.H] = float(f[-1])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--desde", default="2022-01")
    ap.add_argument("--intervalos", nargs="+", default=["1h", "4h"])
    ap.add_argument("--monedas", nargs="+", default=MONEDAS)
    a = ap.parse_args()
    meses = [p.strftime("%Y-%m") for p in pd.period_range(a.desde, pd.Timestamp.utcnow().strftime("%Y-%m"), freq="M")][:-1]
    nombre = "base_binancevision.pkl.gz"
    base = D._leer(nombre, {"velas": {}, "funding": {}, "fuente": "data.binance.vision"})
    s = requests.Session()
    total = 0
    for i, m in enumerate(a.monedas, 1):
        simbolo = f"{m}USDT"
        print(f"  [{i}/{len(a.monedas)}] {simbolo}", flush=True)
        for mes in meses:
            for iv in a.intervalos:
                v = velas_mes(s, simbolo, iv, mes)
                base["velas"].setdefault(iv, {}).setdefault(m, {}).update(v)
                total += len(v)
            base["funding"].setdefault(m, {}).update(funding_mes(s, simbolo, mes))
        D._escribir(nombre, base)
    if total == 0:
        raise SystemExit("No se descargo ninguna vela (¿bloqueado?)")
    base["actualizado"] = int(time.time() * 1000)
    D._escribir(nombre, base)
    print(f"Guardado lab/datos/{nombre} ({total} velas). Para usarlo: LAB_BASE={nombre}")


if __name__ == "__main__":
    main()
