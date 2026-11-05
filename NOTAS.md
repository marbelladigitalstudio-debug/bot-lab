
## 2026-11-05 — familias extra de repos (punto 2)
Añadidas en `lab/extra_tecnicos.py`: supertrend, keltner_ruptura, ichimoku_cierre, kama_tendencia, squeeze_ruptura (reescritas, sin copiar código). Motivo: probar indicadores populares de freqtrade-strategies con los mismos filtros. Test `lab/test_futuro.py` (pesos con datos truncados = pesos completos) superado; incluye control negativo. Limitación: la caché no tiene mínimos reales.

## 2026-11-05 — nuevos filtros: White Reality Check y SPA de Hansen (punto 4)
`lab/validacion.py`: `indices_bootstrap_estacionario` (Politis-Romano 1994) y `spa_hansen` (White 2000; Hansen 2005).
`lab/spa.py --intervalo 4h`: p-valor del máximo de TODAS las configuraciones probadas contra "no operar", y de la mejor
de cada familia en la reserva. Motivo: DSR corrige por nº de pruebas con supuestos normales; el SPA usa bootstrap por
bloques (respeta autocorrelación y colas gordas) y es el estándar para "data snooping". Regla nueva: una candidata debe
además tener p_SPA < 0,05 en la reserva para considerarse. Corregido fallo de supertrend (bandas NaN → siempre 0).
Añadida familia `cambio_regimen` (extra_regimen.py) a petición de Miguel; test de truncado superado.

## 2026-11-05 — caja de herramientas (petición de Miguel)
- `requisitos/` con versiones fijadas por área + `bloqueo.txt` (entorno exacto probado). yfinance fijado a 1.7.0 porque 1.8.0 choca con ccxt (cffi).
- `lab/herramientas/`: descarga_ccxt, descarga_acciones, noticias (RSS+GDELT+VADER), regimen (HMM con filtro hacia delante, ruptures solo diagnóstico), contraste_spa (vs arch), informe_quantstats, avisos (apprise, URL por variable de entorno).
- `datos.cargar` acepta `LAB_BASE` para usar otra base (p. ej. la de Binance). Motivo: historia más larga.
- `lab/extra_hmm.py` (familia hmm_regimen; solo se registra si hmmlearn está instalado). El test de truncado detectó que el arranque dependía de la longitud total: corregido a 60 días fijos.
- `lab/carry_funding.py`: estimación del carry delta-neutral. Positivo en la reserva (+2 a +4 % anual en grandes). Pendiente validar con años de datos y riesgo de base.
- `terceros/`: 15 submódulos fijados a commit (enlaces, no copias).

## 2026-11-05 — ejecución automática en GitHub Actions
`.github/workflows/laboratorio.yml` + `lab/ejecutar_nube.sh`: descarga datos públicos (Hyperliquid ~2,3 años en 4 h;
ccxt Binance/Bybit/OKX desde 2022 si responden), pasa laboratorio 4h/1h, meta-validación, SPA, carry y Monte Carlo y
sube `resultados/` a la rama. Motivo: la sesión en la nube y Miguel no pueden descargar datos; Actions sí tiene red.
Se lanza cambiando `.github/ejecutar.txt`. Sin claves ni órdenes.

## 2026-11-05 — primeros resultados con datos reales (ejecución 3 de Actions)
Hyperliquid (2,3 años en 4h), OKX y archivo público de Binance (4,8 años). Nada pasa los filtros; SPA de la reserva p ≥ 0,22.
OKX no sirve para el carry (la API solo da ~3 meses de funding). Corregida la fecha del commit automático (faltaban comillas).
