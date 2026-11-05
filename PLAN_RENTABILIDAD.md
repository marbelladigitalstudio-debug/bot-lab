# Cómo lo afrontaría si tuviera que sacar rentabilidad de esto

Escrito el 5-nov-2026 tras dos sesiones de laboratorio. Es mi opinión razonada, no una promesa.

## 1. La pregunta que manda: ¿quién me paga y por qué?
En trading, cada euro que se gana lo pierde otro. Antes de cualquier indicador hay que poder decir quién paga:

| Fuente de ganancia | Quién paga | ¿Al alcance de un minorista? | Lo que hemos medido |
|---|---|---|---|
| **Carry de funding** (corto en el perpetuo + largo en el contado) | Los especuladores apalancados en largo | **Sí** | Positivo y estable en la reserva: **+2 a +4 % anual** sobre el capital en monedas grandes (`lab/carry_funding_grandes.txt`). Es lo único que no parece ruido |
| Prima de riesgo de mercado (comprar y mantener) | Nadie: es el premio por aguantar caídas | Sí | Cripto: muy volátil (−50 % es normal). S&P 500: ~8–10 % al año a largo plazo |
| Tendencia a varios meses, cartera diversificada | Inversores que reaccionan tarde | Sí, con ventaja pequeña | No validable con 180 días de datos |
| Indicadores técnicos en 1h/4h | — | La evidencia dice que no tras costes | **0 de ~10.000 configuraciones** pasan los filtros |
| Noticias (velocidad) | Quien lee las noticias más tarde | No: los fondos leen en milisegundos | — |
| Market making | Quien cruza el diferencial con prisa | Difícil: hay que competir con profesionales | Sin datos de libro |

## 2. Lo que haría, en orden
1. **Datos primero (1 tarde en el portátil).** Bajar 3–4 años con `herramientas/descarga_ccxt.py` y 20 años de SPY con
   `herramientas/descarga_acciones.py`. Sin esto, todo lo demás es adivinar.
2. **El carry de funding como base del negocio.** Es una ventaja con explicación económica, de bajo riesgo de precio y
   medible. Toca validarla con 3 años de datos (¿cuánto da en mercado bajista?, ¿cuánto se separan perpetuo y contado?)
   y con costes reales del exchange. Expectativa honesta: entre un 5 y un 15 % anual sobre el capital en buenos años y
   cerca de 0 en los malos.
3. **Una sola apuesta direccional, pequeña y diversificada.** Tendencia lenta (semanas o meses) sobre BTC, ETH y SPY, con
   volatilidad objetivo. Se valida con el SPA en 3+ años, no en 6 meses.
4. **Las noticias, solo hacia delante.** `herramientas/noticias.py` acumula titulares cada día. Dentro de 6 meses se
   comprueba si el sentimiento predice algo. Ahora no hay histórico fiable para validarlo.
5. **Seguimiento en papel 90 días** de lo que pase los filtros. Después, dinero real pequeño (≤10 % de lo previsto),
   como mucho a ¼ de Kelly, con un corte automático si la caída supera el doble de la esperada.

## 3. "Automejorarse todo el rato": la forma segura de hacerlo
La automejora ingenua (probar más y más configuraciones y quedarse con la mejor) **es justo lo que fabrica estrategias
falsas**. Lo hemos visto tres veces hoy: `cambio_regimen` (Sharpe 4 en la búsqueda, −73 % en la reserva), la familia
HMM (−21 %) y la mejor de la búsqueda en general (+1 %). Automejorarse bien significa:
- **Más datos cada día** (`datos.py` y `herramientas/noticias.py` acumulan): esto sí mejora el bot.
- **Más pruebas solo con un listón que sube**: el DSR y el SPA ya penalizan cada prueba nueva.
- **Ideas nuevas con explicación económica**, no más parámetros.
- **Seguimiento hacia delante** como único juez.

Ya está montado: `EJECUTAR_LAB.bat` + `INSTALAR_TAREA_DIARIA.bat` en el portátil. Desde la nube no se puede hacer a
diario porque no hay acceso a los datos de mercado.

## 4. El número que hay que tener en la cabeza
Con 10.000 € y una ventaja real y buena (Sharpe 1, volatilidad del 15–20 %), lo esperable son **unos 600–1.000 € en
5 meses**, con meses en negativo. Con el carry, ~200–500 €. Ganar 2.000 € en 5 meses con 2.000 € exige apostar, no
invertir: las tablas de `INFORME.md` lo cuantifican.
