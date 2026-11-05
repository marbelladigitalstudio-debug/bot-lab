
## 2026-11-05 — familias extra de repos (punto 2)
Añadidas en `lab/extra_tecnicos.py`: supertrend, keltner_ruptura, ichimoku_cierre, kama_tendencia, squeeze_ruptura (reescritas, sin copiar código). Motivo: probar indicadores populares de freqtrade-strategies con los mismos filtros. Test `lab/test_futuro.py` (pesos con datos truncados = pesos completos) superado; incluye control negativo. Limitación: la caché no tiene mínimos reales.
