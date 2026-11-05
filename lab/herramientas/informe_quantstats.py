"""
Informe HTML completo de una serie de rentabilidades con quantstats (Apache-2.0): caidas, meses, VaR, etc.
Uso:  python -m herramientas.informe_quantstats --intervalo 4h --clave "<clave del registro>"
"""
import argparse

import pandas as pd

from herramientas import requiere
import automejora as A
import datos
import estrategias as E
import motor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervalo", default="4h")
    ap.add_argument("--clave", required=True)
    a = ap.parse_args()
    qs = requiere("quantstats", "analisis.txt")
    panel = datos.cargar(a.intervalo)
    reg = pd.read_csv(A._ruta(f"registro_{a.intervalo}.csv"))
    f = reg.loc[reg["clave"] == a.clave].iloc[0]
    s = motor.simular(E.FAMILIAS[f["familia"]]["fn"](panel, A._params_json(f["params"])), panel)
    r = s["ret"].copy()
    r.index = pd.to_datetime(r.index, unit="ms")
    r = (1 + r).resample("1D").prod() - 1
    salida = f"quantstats_{f['familia']}.html"
    qs.reports.html(r, output=salida, title=a.clave[:80], periods_per_year=365)
    print("Informe:", salida)


if __name__ == "__main__":
    main()
