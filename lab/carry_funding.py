"""
Carry de funding DELTA-NEUTRAL (estimacion): corto en el perpetuo + largo en contado de la misma moneda.
El precio se cancela; se cobra el funding cuando es positivo (los largos pagan a los cortos).
Regla (sin mirar el futuro): cada 'mantener' dias, se eligen las monedas cuya media de funding de los ultimos
'dias' supera 'umbral'; reparto igual. Coste: 4 lados (abrir/cerrar perp y contado) por cada cambio.
LIMITACIONES: supone contado disponible y sin coste de base/prestamo; ignora el riesgo de que el perp y el
contado se separen y el margen necesario (~50 % del capital en cada pata con apalancamiento 1-2x).
Uso: python carry_funding.py
"""
import itertools

import numpy as np
import pandas as pd

import comun as C
import datos
import validacion as V


def simular(f, dias, umbral, mantener, coste_lado=C.COSTE_LADO):
    H = 24
    media = f.rolling(dias * H, min_periods=dias * H).mean()
    sel = (media > umbral).astype(float)
    m = np.zeros(len(f), dtype=bool); m[::mantener * H] = True
    sel = sel.where(pd.Series(m, index=f.index), np.nan).ffill().fillna(0.0)
    n = sel.sum(axis=1).replace(0, np.nan)
    W = sel.div(n, axis=0).fillna(0.0)          # fraccion del capital en cada par (perp corto + contado largo)
    W = W * 0.5                                  # la mitad del capital en cada pata
    Wp = W.shift(1).fillna(0.0)
    cobro = (Wp * f).sum(axis=1)                 # corto cobra funding positivo
    giro = (W - W.shift(1).fillna(0.0)).abs().sum(axis=1)
    coste = giro.shift(1).fillna(0.0) * coste_lado * 2   # perp + contado
    return cobro - coste, W


def main(solo_grandes=False):
    p = datos.cargar("1h")
    f = p["funding"]
    if solo_grandes:
        f = f[[c for c in f.columns if c in C.GRANDES]]
        print("== SOLO MONEDAS GRANDES (con contado liquido) ==")
    corte = f.index[int(len(f) * (1 - C.FRACCION_RESERVA))]
    filas = []
    for dias, umbral, mantener in itertools.product([3, 7, 14], [0.0, 0.00001, 0.00003], [1, 7, 14]):
        r, W = simular(f, dias, umbral, mantener)
        rb, rr = r[r.index < corte], r[r.index >= corte]
        filas.append({"dias": dias, "umbral_h": umbral, "mantener": mantener,
                      "anual_busq": rb.mean() * 8760, "anual_res": rr.mean() * 8760,
                      "sharpe_res": rr.mean() / (rr.std() or 1) * np.sqrt(8760), "expo": W.abs().sum(axis=1).mean() * 2})
    t = pd.DataFrame(filas).sort_values("anual_busq", ascending=False)
    mejor = t.iloc[0]
    print("Funding medio anualizado por moneda (todo el periodo, top 10):")
    print((f.mean() * 8760).sort_values(ascending=False).head(10).map("{:+.1%}".format).to_string())
    print("\nTop 5 configuraciones por rentabilidad en la BUSQUEDA (y lo que dieron en la reserva):")
    print(t.head(5).to_string(index=False, float_format=lambda x: f"{x:.4g}"))
    print(f"\nElegida en la busqueda -> reserva: {mejor['anual_res']:+.1%} anual sobre el capital total, "
          f"Sharpe {mejor['sharpe_res']:.1f}. Mediana de las 27 en la reserva: {t['anual_res'].median():+.1%}")


if __name__ == "__main__":
    import sys
    main("--grandes" in sys.argv)
