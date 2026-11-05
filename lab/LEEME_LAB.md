# Laboratorio de automejora (solo simulación)

Una máquina que busca estrategias sola, las apunta todas y solo deja pasar las que sobreviven
a filtros pensados para no engañarse. No opera con dinero real ni guarda claves.

## Cómo se usa
1. **Doble clic en `EJECUTAR_LAB.bat`.** La primera vez descarga 2 años de velas de 4 h, 200 días
   de velas de 1 h y el funding de unas 30 monedas de Hyperliquid (alrededor de 1 hora, porque la API limita el ritmo). Las siguientes veces
   solo descarga lo nuevo.
2. Al terminar se abre `informe_4h.html`. También quedan `informe_1h.html`, `informe_4h.txt`
   (para pegárselo a Claude) y `meta_validacion_4h.txt`.
3. **Para que se mejore sola cada día:** doble clic en `INSTALAR_TAREA_DIARIA.bat`. Así se ejecuta
   a las 14:13, siempre que el portátil esté encendido. Para quitar la tarea: `QUITAR_TAREA_DIARIA.bat`.

## Qué hace cada día
- Amplía la base de datos: Hyperliquid solo da las últimas 5000 velas, pero lo ya guardado no se borra.
- Prueba 600 configuraciones nuevas. El 40 % son al azar y el 60 % son mutaciones de las mejores.
  Además prueba combinaciones de la mejor de cada familia.
- Lo apunta todo en `registro_4h.csv`. **Cuantas más pruebas acumula, más exigente se vuelve**,
  porque el Deflated Sharpe tiene en cuenta cuántas cosas se han probado.
- Pasa por los filtros a la mejor de cada familia:
  - DSR ≥ 0,95
  - Parámetros vecinos estables
  - PBO ≤ 0,5
  - Ninguna moneda aporta más del 50 % del beneficio
  - Positiva en la reserva (datos que la búsqueda nunca ve), con corrección de Bonferroni
  - Sigue siendo positiva con el doble de costes
- A las que pasan les hace **seguimiento hacia delante** desde el día en que se eligieron.
  Esa es la única prueba que de verdad cuenta.

## Regla para pensar en dinero real
Hacen falta al menos 90 días de seguimiento hacia delante con PSR ≥ 0,95, costes reales comprobados
y una explicación de por qué funciona. Aun así, se empieza con poco. Nada de esto ocurre de forma automática.

## Añadir estrategias (así mejora Claude el laboratorio)
Se crea `extra_nombre.py` en esta carpeta con:
```python
FAMILIAS = {"mi_idea": {"fn": funcion, "espacio": {"param": [1, 2, 3]}, "fuente": "de dónde sale"}}
```
`funcion(panel, p)` devuelve pesos (fecha × moneda), usando solo datos hasta el cierre de cada barra.
Se carga sola en la siguiente ejecución. Si pegas `informe_4h.txt` en una conversación con Claude,
puede proponer y escribir familias nuevas a partir de lo que ha fallado.

## Archivos
- `comun.py`: todos los ajustes (costes, filtros, número de pruebas)
- `datos.py`: descarga
- `motor.py`: backtest
- `estrategias.py`: biblioteca de estrategias
- `validacion.py`: DSR, PSR, PBO
- `automejora.py`: el bucle
- `informe.py`: los informes
- `meta_validacion.py`: comprueba si "elegir la mejor del pasado" sirve en estos datos

## Fuentes
- Bailey y López de Prado, *The Deflated Sharpe Ratio* (2014), https://papers.ssrn.com/abstract=2460551
- Bailey, Borwein, López de Prado y Zhu, *The Probability of Backtest Overfitting* (2015), https://papers.ssrn.com/abstract=2326253
- Estrategias de freqtrade-strategies-that-work (paulcpk), https://github.com/paulcpk/freqtrade-strategies-that-work
- Momentum temporal y de sección cruzada en cripto (AUT), https://acfr.aut.ac.nz/__data/assets/pdf_file/0009/918729/Time_Series_and_Cross_Sectional_Momentum_in_the_Cryptocurrency_Market_with_IA.pdf
- Funding como señal (evidencia débil), https://bravenewcoin.com/insights/testing-theory-is-perpetual-swap-funding-rate-predictive
