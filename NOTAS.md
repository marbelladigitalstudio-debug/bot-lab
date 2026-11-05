
## 2026-11-05 — familias extra de repos (punto 2)
Añadidas en `lab/extra_tecnicos.py`: supertrend, keltner_ruptura, ichimoku_cierre, kama_tendencia, squeeze_ruptura (reescritas, sin copiar código). Motivo: probar indicadores populares de freqtrade-strategies con los mismos filtros. Test `lab/test_futuro.py` (pesos con datos truncados = pesos completos) superado; incluye control negativo. Limitación: la caché no tiene mínimos reales.

## 2026-11-05 — nuevos filtros: White Reality Check y SPA de Hansen (punto 4)
`lab/validacion.py`: `indices_bootstrap_estacionario` (Politis-Romano 1994) y `spa_hansen` (White 2000; Hansen 2005).
`lab/spa.py --intervalo 4h`: p-valor del máximo de TODAS las configuraciones probadas contra "no operar", y de la mejor
de cada familia en la reserva. Motivo: DSR corrige por nº de pruebas con supuestos normales; el SPA usa bootstrap por
bloques (respeta autocorrelación y colas gordas) y es el estándar para "data snooping". Regla nueva: una candidata debe
además tener p_SPA < 0,05 en la reserva para considerarse. Corregido fallo de supertrend (bandas NaN → siempre 0).
Añadida familia `cambio_regimen` (extra_regimen.py) a petición de Miguel; test de truncado superado.
