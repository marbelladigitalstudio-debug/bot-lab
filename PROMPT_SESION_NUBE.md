Lee CLAUDE.md. Trabaja sin preguntar y haz commit al terminar cada punto.

1. INVESTIGA GITHUB: busca y revisa los repositorios de trading algorítmico más útiles para este laboratorio (por ejemplo
   freqtrade y freqtrade-strategies, hummingbot, jesse, vectorbt, backtrader, nautilus_trader, QuantConnect Lean, ccxt,
   hyperliquid-python-sdk, microsoft/qlib, FinRL, pandas-ta y otros que encuentres con buena reputación).
   Para cada uno: qué aporta, licencia, último commit, si sirve para nosotros. Escríbelo en `referencias/REPOS.md`.
2. TRAE IDEAS PROBADAS: de los repos con licencia compatible, porta a `lab/extra_*.py` las estrategias e indicadores que tengan
   sentido para cripto en 1h/4h (no copies a ciegas: reescribe en el formato FAMILIAS, con su fuente y licencia anotadas).
   Pasa a cada familia nueva el test de mirar el futuro.
3. EJECUTA EL LABORATORIO con la caché: `cd lab && python automejora.py --intervalo 4h --sin-descarga --pruebas 3000`
   y lo mismo con `--intervalo 1h`, y `python meta_validacion.py --intervalo 4h`.
4. MEJORA LOS FILTROS si encuentras métodos mejores en la literatura o en los repos (por ejemplo walk-forward combinatorio,
   bootstrap por bloques, test de White Reality Check / SPA de Hansen). Documenta el motivo.
5. INFORME: `INFORME.md` en español claro: qué repos sirven, qué familias se añadieron, qué pasa los filtros y qué no, y qué
   haría falta (datos, capital, tiempo) para tener una ventaja real. Sin promesas: si nada pasa, dilo.
