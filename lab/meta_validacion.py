"""
¿SIRVE DE ALGO ELEGIR "LA MEJOR DEL PASADO"?
============================================
Prueba al propio metodo del laboratorio. Parte la historia en bloques consecutivos y,
para cada par (bloque A -> bloque siguiente B), mira si las configuraciones que mejor
fueron en A tambien van mejor en B.

  rho      : correlacion de rangos entre el Sharpe en A y en B (0 = el pasado no dice nada)
  top 1 %  : Sharpe medio en B de las mejores 1 % de A, frente a la mediana de todas en B

Si rho ronda 0 y el top 1 % no supera a la mediana, buscar "la mejor" en el pasado es
elegir ruido, por muchas pruebas que se hagan.

  python meta_validacion.py --intervalo 4h --bloques 5
"""
import argparse

import numpy as np
import pandas as pd

import automejora as A
import datos
import estrategias as E
import motor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervalo", default="4h")
    ap.add_argument("--bloques", type=int, default=5)
    ap.add_argument("--max", type=int, default=3000)
    a = ap.parse_args()
    panel = datos.cargar(a.intervalo)
    lab = A.Lab(a.intervalo, panel, 0, 0)
    reg = lab.reg[lab.reg["familia"] != "conjunto"]
    if reg.empty:
        raise SystemExit("Registro vacio: ejecuta antes automejora.py")
    reg = reg.sample(min(a.max, len(reg)), random_state=0)
    idx = lab.idx
    validos = idx >= lab.ini
    pos = np.where(validos)[0]
    trozos = np.array_split(pos, a.bloques)
    sh = {i: [] for i in range(a.bloques)}
    fams = []
    print(f"Evaluando {len(reg)} configuraciones en {a.bloques} bloques...")
    for j, (_, f) in enumerate(reg.iterrows()):
        W = E.FAMILIAS[f["familia"]]["fn"](panel, A._params_json(f["params"]))
        r = motor.simular(W, panel)["ret"].values
        for i, t in enumerate(trozos):
            x = r[t]
            sh[i].append(x.mean() / x.std() * np.sqrt(len(x)) if x.std() > 0 else 0.0)
        fams.append(f["familia"])
        if (j + 1) % 500 == 0:
            print(f"   {j + 1}")
    S = pd.DataFrame(sh)
    S["familia"] = fams
    lin = [f"META-VALIDACION {a.intervalo}: {len(S)} configuraciones, {a.bloques} bloques de "
           f"~{len(trozos[0]) / E.barras_dia(panel):.0f} dias", "",
           "bloque A -> B | rho (rangos) | B: mediana todas | B: top 1 % de A | B: top 10 % de A | B: mejor de A"]
    rhos = []
    for i in range(a.bloques - 1):
        a_, b_ = S[i], S[i + 1]
        rho = a_.rank().corr(b_.rank())
        rhos.append(rho)
        q1, q10 = a_.quantile(0.99), a_.quantile(0.90)
        lin.append(f"   {i + 1} -> {i + 2}      | {rho:+.2f}        | {b_.median():+.2f}            | "
                   f"{b_[a_ >= q1].mean():+.2f}            | {b_[a_ >= q10].mean():+.2f}             | {b_[a_.idxmax()]:+.2f}")
    lin += ["", f"rho medio {np.mean(rhos):+.2f}  (las cifras de B son Sharpe del bloque sin anualizar x raiz(n))", "",
            "Por familia (rho medio entre bloques consecutivos):"]
    for fam, g in S.groupby("familia"):
        rr = [g[i].rank().corr(g[i + 1].rank()) for i in range(a.bloques - 1)]
        lin.append(f"   {fam:22} {np.nanmean(rr):+.2f}   ({len(g)} configs)")
    lin += ["", "Lectura: rho cerca de 0 = el ranking del pasado no predice el siguiente bloque.",
            "Positivo y estable en todos los pares = hay algo de persistencia que vale la pena seguir."]
    texto = "\n".join(lin)
    print(texto)
    with open(A._ruta(f"meta_validacion_{a.intervalo}.txt"), "w", encoding="utf-8") as fh:
        fh.write(texto + "\n")


if __name__ == "__main__":
    main()
