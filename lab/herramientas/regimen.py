"""
Deteccion de regimen sin mirar el futuro.
  - hmm_regimen: HMM gaussiano (hmmlearn, BSD) re-entrenado hacia delante cada 'cada' barras con SOLO el pasado.
    Devuelve, para cada barra, la probabilidad filtrada (no suavizada) del regimen de mayor volatilidad.
  - cambios_estructurales: ruptures (BSD-2). OJO: usa toda la serie -> SOLO para diagnostico, nunca como senal.
"""
import numpy as np
import pandas as pd

from herramientas import requiere


def _rasgos(precio, n_vol=24):
    r = np.log(precio).diff()
    # en % para que la covarianza no sea minuscula (evita matrices casi singulares)
    return 100 * pd.concat([r, r.rolling(n_vol).std()], axis=1).dropna()


def _log_emision(modelo, X):
    """log N(x | media_k, cov_k) para cada barra y estado (covarianza completa)."""
    K, d = modelo.means_.shape
    out = np.empty((len(X), K))
    for k in range(K):
        cov = modelo.covars_[k]
        cov = cov + 1e-6 * np.eye(d)
        inv, (_, logdet) = np.linalg.pinv(cov), np.linalg.slogdet(cov)
        z = X - modelo.means_[k]
        out[:, k] = -0.5 * (np.einsum("ij,jk,ik->i", z, inv, z) + logdet + d * np.log(2 * np.pi))
    return out


def hmm_regimen(precio, estados=2, minimo=500, cada=168, semilla=0):
    """Probabilidad FILTRADA del regimen de alta volatilidad. El modelo se entrena con X[:fin] y luego
    solo se usa hacia delante hasta el siguiente re-entreno (filtro de avance: P(estado_t | x_1..x_t))."""
    hmm = requiere("hmmlearn.hmm", "analisis.txt")
    X = _rasgos(precio)
    V = X.values
    p_alta = pd.Series(np.nan, index=precio.index)
    alfa = None
    for ini in range(minimo, len(V), cada):
        modelo = hmm.GaussianHMM(n_components=estados, covariance_type="full", n_iter=100, random_state=semilla,
                                 min_covar=1e-3)
        modelo.fit(V[:ini])
        alto = int(np.argmax(modelo.covars_[:, 0, 0]))   # estado con mas varianza de la rentabilidad
        # estado de partida: filtro sobre el tramo de entrenamiento (solo pasado)
        le = _log_emision(modelo, V[:ini])
        a = modelo.startprob_.copy()
        for t in range(ini):
            a = (a if t == 0 else a @ modelo.transmat_) * np.exp(le[t] - le[t].max())
            a /= a.sum()
        le = _log_emision(modelo, V[ini:ini + cada])
        for j in range(len(le)):
            a = (a @ modelo.transmat_) * np.exp(le[j] - le[j].max())
            a /= a.sum()
            p_alta.loc[X.index[ini + j]] = a[alto]
    return p_alta


def cambios_estructurales(serie, penal=10):
    rpt = requiere("ruptures", "analisis.txt")
    x = serie.dropna().values.reshape(-1, 1)
    puntos = rpt.Pelt(model="rbf").fit(x).predict(pen=penal)
    return [serie.dropna().index[i - 1] for i in puntos[:-1]]
