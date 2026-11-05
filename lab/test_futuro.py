"""Test de mirar el futuro: pesos con datos cortados == pesos con datos completos en las barras comunes."""
import sys
import numpy as np
import pandas as pd
import datos
import estrategias as E


def recorta(panel, k):
    return {a: (b.iloc[:k] if isinstance(b, pd.DataFrame) else b) for a, b in panel.items()}


def main(iv="4h", familias=None, n_params=4, seed=1):
    panel = datos.cargar(iv)
    N = len(panel["close"])
    rng = np.random.default_rng(seed)
    ok = True
    for fam in familias or list(E.FAMILIAS):
        for _ in range(n_params):
            p = {k: v[rng.integers(len(v))] for k, v in E.FAMILIAS[fam]["espacio"].items()}
            Wf = E.FAMILIAS[fam]["fn"](panel, p)
            peor = 0.0
            for k in (int(N * .5), int(N * .8)):
                Wc = E.FAMILIAS[fam]["fn"](recorta(panel, k), p)
                a = Wf.reindex(Wc.index).fillna(0.0).values
                b = Wc.fillna(0.0).values
                peor = max(peor, float(np.abs(a - b).max()))
            bien = peor < 1e-9
            ok &= bien
            if not bien:
                print(f"  MIRA EL FUTURO: {fam} {p} dif={peor:.3g}")
        print(f"{fam}: {'ok' if ok else 'REVISAR'}")
    return ok


if __name__ == "__main__":
    f = sys.argv[2:] or None
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else "4h", f) else 1)
