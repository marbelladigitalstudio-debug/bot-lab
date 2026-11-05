# Herramientas opcionales

Se ejecutan desde la carpeta `lab/`:

| Comando | Qué hace | Necesita |
|---|---|---|
| `python -m herramientas.descarga_ccxt --desde 2022-01-01` | Historia larga de Binance (perpetuos, funding) en `datos/base_binanceusdm.pkl.gz` | `requisitos/datos.txt` |
| `LAB_BASE=base_binanceusdm.pkl.gz python automejora.py --intervalo 4h` | El laboratorio con esa historia | — |
| `python -m herramientas.descarga_acciones` | S&P 500, ETFs y VIX diarios en `datos/acciones_1d.pkl.gz` | `requisitos/datos.txt` |
| `python -m herramientas.noticias` | Acumula titulares y su sentimiento (ejecutar a diario) | `requisitos/noticias.txt` |
| `python -m herramientas.contraste_spa` | Compara nuestro SPA con el de `arch` | `requisitos/analisis.txt` |
| `python -m herramientas.informe_quantstats --clave "<clave>"` | Informe HTML de una configuración del registro | `requisitos/analisis.txt` |
| `python -m herramientas.avisos "texto"` | Aviso por Telegram, correo, etc. (variable `BOT_AVISOS`) | `requisitos/avisos.txt` |

En Windows, `set LAB_BASE=...` y, en otra línea, el comando.

Ninguna herramienta usa claves privadas ni manda órdenes. Todo lo que genera una señal pasa por `test_futuro.py`.
