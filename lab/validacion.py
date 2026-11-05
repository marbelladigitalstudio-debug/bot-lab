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


# ---------------------------------------------------------------- bootstrap y SPA (anadido 2026-11-05)
def indices_bootstrap_estacionario(T, bloque_medio, B, rng):
    """Politis y Romano (1994): bloques de longitud geometrica con media bloque_medio. Devuelve B x T indices."""
    p = 1.0 / max(bloque_medio, 1)
    idx = np.empty((B, T), dtype=np.int64)
    idx[:, 0] = rng.integers(T, size=B)
    nuevo = rng.random((B, T)) < p
    salto = rng.integers(T, size=(B, T))
    for t in range(1, T):
        idx[:, t] = np.where(nuevo[:, t], salto[:, t], (idx[:, t - 1] + 1) % T)
    return idx


def spa_hansen(M, bloque_medio=24, B=1000, semilla=0):
    """White Reality Check (2000) y SPA de Hansen (2005) contra el referente 'no operar' (rentabilidad 0).
    M: barras x estrategias (rentabilidad neta por barra). H0: ninguna supera al referente.
    Devuelve dict con p_rc (White), p_spa (Hansen, version consistente) y la mejor columna.
    Corrige el sesgo de busqueda: la significancia se mide contra el maximo de TODAS las probadas."""
    M = np.asarray(M, dtype=float)
    M = M[:, M.std(axis=0) > 0]
    T, K = M.shape
    if K == 0 or T < 50:
        return {"p_rc": float("nan"), "p_spa": float("nan"), "k": K}
    rng = np.random.default_rng(semilla)
    d = M.mean(axis=0)
    idx = indices_bootstrap_estacionario(T, bloque_medio, B, rng)
    medias = np.empty((B, K))
    for b in range(B):
        medias[b] = M[idx[b]].mean(axis=0)
    omega = np.sqrt(T) * medias.std(axis=0)              # desviacion de sqrt(T)*media
    omega = np.where(omega > 0, omega, 1e-12)
    rt = np.sqrt(T)
    # White: estadistico sin estandarizar, centrado en d
    v_rc = rt * d.max()
    v_rc_b = (rt * (medias - d)).max(axis=1)
    p_rc = float((v_rc_b >= v_rc).mean())
    # Hansen SPA consistente: estandarizado, y se recentran solo las que no son claramente malas
    t_spa = max(0.0, (rt * d / omega).max())
    umbral = -np.sqrt(2 * np.log(np.log(T))) * omega / rt
    mu_c = np.where(d >= umbral, d, 0.0)
    t_b = np.maximum(0.0, (rt * (medias - mu_c) / omega).max(axis=1))
    p_spa = float((t_b >= t_spa).mean())
    return {"p_rc": p_rc, "p_spa": p_spa, "k": K, "mejor": int(np.argmax(d / omega))}
