"""
Comprueba nuestro spa_hansen (validacion.py) contra la implementacion de referencia de arch (NCSA, Kevin Sheppard).
Dos casos sinteticos: (a) ninguna estrategia tiene ventaja -> p alto; (b) una tiene ventaja real -> p bajo.
Uso:  python -m herramientas.contraste_spa
"""
import numpy as np

from herramientas import requiere
import validacion as V


def casos(T=1500, K=200, semilla=1):
    rng = np.random.default_rng(semilla)
    nulo = rng.standard_t(4, size=(T, K)) * 0.01
    con = nulo.copy()
    con[:, 0] += 0.0012           # Sharpe por barra ~0,1 en una de 200
    return {"sin ventaja": nulo, "una con ventaja": con}


def main():
    arch_b = requiere("arch.bootstrap", "analisis.txt")
    print("caso            | nuestro p_SPA | arch p_SPA (consistente) | nuestro p_White")
    for nombre, M in casos().items():
        nuestro = V.spa_hansen(M, bloque_medio=10, B=1000, semilla=0)
        # arch trabaja con PERDIDAS: perdida = -rentabilidad; referencia = 0
        spa = arch_b.SPA(np.zeros(len(M)), -M, block_size=10, reps=1000, bootstrap="stationary", seed=0)
        spa.compute()
        print(f"{nombre:15s} | {nuestro['p_spa']:.3f}         | {spa.pvalues['consistent']:.3f}                    "
              f"| {nuestro['p_rc']:.3f}")


if __name__ == "__main__":
    main()
