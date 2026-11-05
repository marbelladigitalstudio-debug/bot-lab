"""
Punto 6 (OBJETIVO.md): traducir el objetivo a numeros y Monte Carlo por bloques sobre rentabilidades FUERA de muestra.
Candidatas (sin elegir nada mirando la reserva):
  - cartera_familias: media de la mejor de cada familia (elegida en la busqueda) en la reserva.
  - mejor_busqueda: la configuracion con mejor Sharpe en la busqueda (lo que haria un bot "que se automejora"), en la reserva.
  - mercado: comprar y mantener todas las monedas a partes iguales (referencia).
Cada una tambien "sin ventaja": misma serie con la media restada (lo que dice el SPA: p ~ 0,5).
Apalancamiento L: rentabilidad L*r por barra; si el capital toca 0 se liquida.
Uso: python objetivo_mc.py --intervalo 4h
"""
import argparse
import pickle
from statistics import NormalDist

import numpy as np
import pandas as pd

import comun as C
import datos
import validacion as V

CAPITALES = [1000, 2000, 5000, 10000]
OBJETIVOS = [2000, 5000]
MESES = 5


def traduccion():
    T = MESES / 12
    filas = ["| Capital | Objetivo | Rentab. en 5 meses | Equivale anual | Sharpe mínimo (Kelly, 50 % de lograrlo) | Apalanc. Kelly si vol 60 %/año |",
             "|---|---|---|---|---|---|"]
    for obj in OBJETIVOS:
        for K in CAPITALES:
            r = obj / K
            anual = (1 + r) ** (12 / MESES) - 1
            # con apalancamiento optimo (Kelly) el crecimiento logaritmico es S^2/2 por ano
            S = np.sqrt(2 * np.log(1 + r) / T)
            filas.append(f"| {K:,} € | +{obj:,} € | +{r:.0%} | +{anual:.0%} | {S:.1f} | x{S / 0.6:.1f} |".replace(",", "."))
    return "\n".join(filas)


def simular(ret, L, K, obj, barras, B=4000, bloque=6, semilla=0):
    rng = np.random.default_rng(semilla)
    x = np.asarray(ret, dtype=float)
    idx = V.indices_bootstrap_estacionario(len(x), bloque, B, rng)
    # se alargan los indices hasta 'barras' repitiendo el proceso
    tiras = [idx]
    while sum(t.shape[1] for t in tiras) < barras:
        tiras.append(V.indices_bootstrap_estacionario(len(x), bloque, B, rng))
    idx = np.concatenate(tiras, axis=1)[:, :barras]
    r = np.clip(L * x[idx], -1.0, None)
    eq = np.cumprod(1 + r, axis=1)
    muerto = np.minimum.accumulate(eq, axis=1) <= 0
    eq = np.where(muerto, 0.0, eq)
    final = eq[:, -1]
    p_obj = float((final * K >= K + obj).mean())
    p_50 = float((eq.min(axis=1) <= 0.5).mean())
    return p_obj, p_50, float(np.median(final) - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervalo", default="4h")
    a = ap.parse_args()
    iv = a.intervalo
    with open(f"reserva_{iv}.pkl", "rb") as fh:
        d = pickle.load(fh)
    res = pd.DataFrame(d["reserva"])
    busq = d["busqueda_mejores"]
    mejor = max(busq, key=lambda k: busq[k].mean() / (busq[k].std() or 1))
    panel = datos.cargar(iv)
    mkt = panel["close"].pct_change(fill_method=None).mean(axis=1).reindex(res.index).fillna(0.0)
    cands = {"cartera_familias": res.mean(axis=1), "mejor_busqueda": res[mejor], "mercado": mkt}
    ba = C.BARRAS_ANO[iv]
    barras = int(ba * MESES / 12)
    bloque = max(1, 24 // (C.MS_INTERVALO[iv] // C.H))
    out = [f"## Monte Carlo {iv} (bootstrap estacionario, bloque medio 1 día, 4000 caminos, {barras} barras = 5 meses)",
           f"Reserva: {len(res)} barras ({pd.to_datetime(res.index[0], unit='ms'):%d/%m/%y} → {pd.to_datetime(res.index[-1], unit='ms'):%d/%m/%y}). "
           f"`mejor_busqueda` = {mejor.split('|')[0]}.", ""]
    for nombre, s in cands.items():
        sh = s.mean() / (s.std() or 1) * np.sqrt(ba)
        out.append(f"- **{nombre}**: Sharpe reserva {sh:+.2f}, rentab. anualizada {s.mean() * ba:+.0%}, vol anual {s.std() * np.sqrt(ba):.0%}")
    out.append("")
    for obj in OBJETIVOS:
        out += [f"### Objetivo +{obj:,} € en 5 meses".replace(",", "."), "",
                "| Candidata | Ventaja | Apal. | " + " | ".join(f"{K:,} €: P(obj) / P(−50 %)".replace(",", ".") for K in CAPITALES) + " |",
                "|---|---|---|" + "---|" * len(CAPITALES)]
        for nombre, s in cands.items():
            for etiqueta, serie in (("la de la reserva", s), ("cero (SPA)", s - s.mean())):
                for L in (1, 2, 3, 5, 10):
                    celdas = []
                    for K in CAPITALES:
                        p, q, _ = simular(serie.values, L, K, obj, barras, bloque=bloque)
                        celdas.append(f"{p:.0%} / {q:.0%}")
                    out.append(f"| {nombre} | {etiqueta} | x{L} | " + " | ".join(celdas) + " |")
        out.append("")
    txt = "\n".join(out)
    with open(f"objetivo_mc_{iv}.md", "w", encoding="utf-8") as fh:
        fh.write("# Traducción del objetivo\n\n" + traduccion() + "\n\n" + txt + "\n")
    print(traduccion()); print(txt)


if __name__ == "__main__":
    main()
