"""
Herramientas contra el autoengano estadistico.

- PSR  (Probabilistic Sharpe Ratio, Bailey y Lopez de Prado 2012): probabilidad de que el Sharpe
       real sea mayor que un umbral, teniendo en cuenta la longitud, la asimetria y las colas.
- DSR  (Deflated Sharpe Ratio, Bailey y Lopez de Prado 2014): PSR contra el Sharpe maximo que
       saldria POR AZAR despues de probar N estrategias. Cuantas mas pruebas, mas exigente.
- PBO  (Probability of Backtest Overfitting, CSCV, Bailey et al. 2015): con que frecuencia la
       mejor configuracion dentro de la muestra queda por debajo de la mediana fuera de ella.
- N efectivo: las pruebas estan muy correlacionadas; se estima cuantas son "independientes".
"""
from itertools import combinations

import numpy as np
from statistics import NormalDist

_N = NormalDist()


class norm:  # sin scipy (puede no estar instalado en el portatil)
    cdf = staticmethod(_N.cdf)

    @staticmethod
    def ppf(p):
        return _N.inv_cdf(min(max(p, 1e-12), 1 - 1e-12))

EULER = 0.5772156649


def psr(sr, n, asim, curt, sr0=0.0):
    """sr y sr0 por barra; curt = curtosis (no exceso; normal = 3)."""
    if n < 3:
        return 0.0
    den = 1 - asim * sr + (curt - 1) / 4 * sr ** 2
    den = np.sqrt(max(den, 1e-12))
    return float(norm.cdf((sr - sr0) * np.sqrt(n - 1) / den))


def sr_esperado_maximo(var_sr, n_pruebas):
    """Sharpe (por barra) maximo esperado por azar entre n_pruebas independientes."""
    if n_pruebas <= 1 or var_sr <= 0:
        return 0.0
    return float(np.sqrt(var_sr) * ((1 - EULER) * norm.ppf(1 - 1 / n_pruebas)
                                    + EULER * norm.ppf(1 - 1 / (n_pruebas * np.e))))


def dsr(sr, n, asim, curt, var_sr, n_pruebas):
    return psr(sr, n, asim, curt, sr_esperado_maximo(var_sr, n_pruebas))


def n_efectivo(matriz):
    """matriz: barras x pruebas. Ratio de participacion de los autovalores de la correlacion."""
    M = np.asarray(matriz, dtype=float)
    M = M[:, M.std(axis=0) > 0]
    if M.shape[1] < 2:
        return float(M.shape[1])
    if M.shape[1] > 1500:
        idx = np.random.default_rng(0).choice(M.shape[1], 1500, replace=False)
        M = M[:, idx]
        factor = matriz.shape[1] / 1500
    else:
        factor = 1.0
    R = np.corrcoef(M, rowvar=False)
    R = np.nan_to_num(R)
    lam = np.sort(np.clip(np.linalg.eigvalsh(R), 0, None))[::-1]
    # componentes necesarias para explicar el 95 % de la varianza (el ratio de participacion
    # se queda corto cuando un factor comun, el mercado, domina todas las pruebas)
    n95 = int(np.searchsorted(np.cumsum(lam) / lam.sum(), 0.95) + 1)
    return float(min(matriz.shape[1], n95 * factor))


def pbo(matriz, bloques=10):
    """CSCV. matriz: barras x configuraciones (rentabilidad por barra). Devuelve (pbo, n_combinaciones)."""
    M = np.asarray(matriz, dtype=float)
    T, N = M.shape
    if N < 4 or T < bloques * 20:
        return float("nan"), 0
    trozos = np.array_split(np.arange(T), bloques)
    malas = total = 0
    for combo in combinations(range(bloques), bloques // 2):
        dentro = np.concatenate([trozos[i] for i in combo])
        fuera = np.concatenate([trozos[i] for i in range(bloques) if i not in combo])
        def sharpe(ix):
            x = M[ix]
            s = x.std(axis=0)
            return np.where(s > 0, x.mean(axis=0) / np.where(s > 0, s, 1), -np.inf)
        sd, sf = sharpe(dentro), sharpe(fuera)
        mejor = int(np.argmax(sd))
        rango = (sf < sf[mejor]).sum() / (N - 1)     # 0 = la peor fuera, 1 = la mejor
        malas += rango < 0.5
        total += 1
    return malas / total, total
