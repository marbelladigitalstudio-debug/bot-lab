"""
Filtro adicional (punto 4): Reality Check de White y SPA de Hansen sobre TODO lo probado.
  1) Busqueda: matriz barras x configuraciones del registro (todas las probadas) -> p del maximo.
  2) Reserva: la mejor de cada familia (elegida en la busqueda) evaluada en la reserva -> p del conjunto.
Guarda las rentabilidades de reserva de cada candidata en reserva_<iv>.pkl para el Monte Carlo.
Uso: python spa.py --intervalo 4h [--max 3000]
"""
import argparse
import pickle

import numpy as np
import pandas as pd

import automejora as A
import comun as C
import datos
import estrategias as E
import motor
import validacion as V


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervalo", default="4h")
    ap.add_argument("--max", type=int, default=3000)
    ap.add_argument("--B", type=int, default=1000)
    a = ap.parse_args()
    iv = a.intervalo
    panel = datos.cargar(iv)
    lab = A.Lab(iv, panel, 0, 0)
    reg = lab.reg[lab.reg["familia"].isin(E.FAMILIAS)].copy()
    if len(reg) > a.max:
        reg = reg.sample(a.max, random_state=0)
    bd = E.barras_dia(panel)
    busq, res = {}, {}
    for _, f in reg.iterrows():
        try:
            s = motor.simular(E.FAMILIAS[f["familia"]]["fn"](panel, A._params_json(f["params"])), panel)
        except Exception:
            continue
        busq[f["clave"]] = s["ret"][lab.m_busq].values
        res[f["clave"]] = (f["familia"], s["ret"][lab.m_res])
    Mb = np.column_stack(list(busq.values()))
    r1 = V.spa_hansen(Mb, bloque_medio=bd, B=a.B)
    # mejor de cada familia en la busqueda
    reg["sh"] = [np.mean(busq[k]) / (np.std(busq[k]) or 1) if k in busq else -9 for k in reg["clave"]]
    mejores = reg.sort_values("sh", ascending=False).groupby("familia").head(1)
    Mr = np.column_stack([res[k][1].values for k in mejores["clave"]])
    r2 = V.spa_hansen(Mr, bloque_medio=bd, B=a.B)
    ba = C.BARRAS_ANO[iv]
    lineas = [f"SPA / REALITY CHECK {iv}: {Mb.shape[1]} configuraciones, {Mb.shape[0]} barras de busqueda",
              f"  Busqueda (todas): p White = {r1['p_rc']:.3f} | p SPA Hansen = {r1['p_spa']:.3f}",
              f"  Reserva (mejor de cada familia, {Mr.shape[1]}): p White = {r2['p_rc']:.3f} | p SPA = {r2['p_spa']:.3f}",
              "  p < 0.05 significaria que al menos una supera a 'no operar' tras corregir por la busqueda.",
              "", "familia | sharpe_res_anual | anual_res"]
    for _, f in mejores.iterrows():
        r = res[f["clave"]][1]
        lineas.append(f"  {f['familia']:22s} {r.mean() / (r.std() or 1) * np.sqrt(ba):+.2f} | {r.mean() * ba:+.1%}")
    txt = "\n".join(lineas)
    print(txt)
    with open(f"spa_{iv}.txt", "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    with open(f"reserva_{iv}.pkl", "wb") as fh:
        pickle.dump({"busqueda_mejores": {k: pd.Series(busq[k]) for k in mejores["clave"]},
                     "reserva": {k: res[k][1] for k in mejores["clave"]}, "iv": iv}, fh)


if __name__ == "__main__":
    main()
