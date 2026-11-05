# bot-lab: laboratorio de estrategias de trading de Miguel (solo simulación)

Miguel del Valle prueba estrategias de cripto (Hyperliquid) en simulación. NUNCA se opera con dinero real ni se guardan claves.

## Qué hay
- `lab/`: laboratorio de automejora en Python (numpy + pandas). `estrategias.py` tiene 12 familias; `automejora.py` prueba
  configuraciones, las registra y las pasa por filtros anti-sobreajuste (DSR, estabilidad, PBO, reserva con Bonferroni,
  costes x2) y hace seguimiento hacia delante. `meta_validacion.py` mide si "la mejor del pasado" predice el siguiente bloque.
- `cache_funding.pkl.gz`: 180 días (abr-oct 2026) de velas de 1 h (solo apertura y máximo) y funding de 40 monedas de Hyperliquid.
  `datos.cargar()` la usa si no hay datos propios. En la nube seguramente no hay acceso a la API de Hyperliquid: usa esta caché.
- `lab/herramientas/` (datos ccxt/yfinance, noticias, régimen HMM, SPA de arch, avisos) y `requisitos/` con versiones fijadas;
  `terceros/` son submódulos de referencia (no `--recursive`). Mapa completo: `referencias/HERRAMIENTAS.md`. Plan: `PLAN_RENTABILIDAD.md`.
- Para añadir estrategias sin tocar el núcleo: `lab/extra_<nombre>.py` con `FAMILIAS = {...}` (ver LEEME_LAB.md).

## Resultado actual (honesto)
Ninguna de ~6.000 configuraciones pasa los filtros. Elegir la mejor del pasado no predice el mes siguiente (rho ≈ 0).
El objetivo NO es encontrar algo que "parezca" ganar, sino algo que sobreviva a los filtros y al seguimiento hacia delante.

## Reglas
- Solo código de terceros con licencia que lo permita. Anota repo, commit y licencia en `referencias/MANIFIESTO.md`.
- No ejecutes scripts de terceros que manden órdenes, pidan claves privadas o instalen cosas solos. Léelos antes.
- No uses `npx -y` ni instales paquetes sin versión fijada.
- Sin mirar el futuro: toda señal usa solo datos hasta el cierre de la barra (el motor ya aplica el desfase). Prueba nueva
  familia con el test de truncado (calcular pesos con datos cortados y comparar con los completos).
- Cada cambio de reglas se apunta en `NOTAS.md` con fecha y motivo.
