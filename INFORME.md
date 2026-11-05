# Informe de la sesión en la nube: 5 de noviembre de 2026

**Resumen:** ninguna de las ~6.000 configuraciones nuevas (más ~4.500 de 4 h y ~4.000 de 1 h acumuladas) pasa los
filtros. El test nuevo (SPA de Hansen, que corrige por todo lo probado) no encuentra nada que supere a "no operar":
p ≈ 0,4–0,7, y haría falta p < 0,05. Elegir la mejor del pasado sigue sin predecir el bloque siguiente (rho medio −0,12).
**Con los datos que hay, el objetivo de +2.000 € en 5 meses no es alcanzable con riesgo razonable** salvo con
10.000 € o más y aceptando que sea casi una apuesta. Lo explico abajo.

Limitación importante: desde la nube el proxy bloquea Hyperliquid, Binance, Yahoo, Stooq y FRED. **No he podido descargar
datos del S&P 500 ni datos nuevos de cripto.** Todo está hecho con `cache_funding.pkl.gz` (180 días, sin mínimos reales).

## 1. Repos de GitHub (detalle en `referencias/REPOS.md`)
| Sirve | Para qué |
|---|---|
| freqtrade / freqtrade-strategies (GPL-3.0) | Ideas de indicadores. Solo se reescriben las fórmulas; no se copia código |
| ccxt (MIT) | Descargar históricos largos de muchos exchanges cuando haya red (en el portátil) |
| hummingbot (Apache-2.0) | Market making. Exige operar en vivo y datos del libro de órdenes, que no tenemos |
| hyperliquid-python-sdk (MIT) | Solo para ejecución; no hace falta para simular |
| qlib (MIT) | Método de evaluación de factores (IC, ventanas móviles) |
| No sirven | vectorbt (Commons Clause), backtrader (abandonado desde 2023), FinRL (RL con 180 días = sobreajuste seguro), nautilus/Lean (demasiado pesados para esto), pandas-ta (licencia no verificable) |

Ningún repo trae una ventaja hecha. Las "estrategias que funcionan" de estos repos son indicadores clásicos, y el
laboratorio ya los prueba.

## 2. Familias añadidas
- `lab/extra_tecnicos.py`: **supertrend, keltner_ruptura, ichimoku_cierre, kama_tendencia, squeeze_ruptura**.
- `lab/extra_regimen.py`: **cambio_regimen**, lo que pediste: usar una estrategia cuando el mercado va en tendencia
  y otra cuando va lateral. Mide el régimen con el ratio de eficiencia de Kaufman, por moneda o con BTC.
- Las 6 pasan el test de mirar el futuro (`lab/test_futuro.py`, que calcula los pesos con datos cortados y los compara
  con los datos completos). El test incluye un control negativo: una familia tramposa, y la detecta.
- Corregido durante la sesión: supertrend daba siempre 0 por bandas iniciales NaN.

## 3. Resultado del laboratorio
| | 4 h | 1 h |
|---|---|---|
| Pasan los filtros | **0** de 18 familias | **0** |
| Sharpe máximo que saldría por azar | ~4,4 | ~4,7 |
| Mejor DSR | 0,84 (conjunto); hace falta 0,95 | 0,88 |
| SPA Hansen, búsqueda (todas) | p = 0,71 | p = 0,42 |
| SPA Hansen, reserva (mejor de cada familia) | p = 0,44 | p = 0,81 |
| Meta-validación (rho entre bloques) | −0,12 | (archivo anterior: ≈0) |

- `cambio_regimen` tuvo buen Sharpe en la búsqueda (3,95) y en la reserva perdió (−73 % anualizado): es el caso típico
  de sobreajuste. Cambiar de estrategia según el régimen añade parámetros, y con 6 meses de datos eso empeora el problema.
- Algunas familias salen positivas en la reserva (keltner, ema_precio_umbral, funding_contrario). Pero esa reserva
  (sept-oct 2026) fue alcista, el mercado ganó +119 % anualizado, y su correlación con el mercado es ≈0,45. Es beta, no ventaja.
- La mejor configuración de la búsqueda (bollinger_reversion), que es la que elegiría un bot "que se automejora",
  dio +1 % anualizado en la reserva. Es decir, nada.

## 4. Filtros mejorados
- **Reality Check de White y SPA de Hansen** con bootstrap estacionario por bloques (`lab/validacion.py`, `lab/spa.py`).
  Comparan el máximo de todo lo probado con "no operar" y respetan la autocorrelación y las colas gordas.
  Regla nueva (apuntada en NOTAS.md): para considerar una candidata, debe tener p_SPA < 0,05 en la reserva.
- Límite: `spa.py` usa como mucho 3.000 configuraciones del registro, elegidas al azar, para que no tarde demasiado.

## 5. Qué haría falta para tener una ventaja real
1. **Datos**: al menos 2–4 años de velas de 1 h/4 h con mínimos reales, y funding. En el portátil se pueden descargar con
   `datos.py`, o con ccxt para Binance/Bybit. Con 180 días, cualquier cosa con más de 2–3 parámetros es indistinguible del azar.
2. **Ventajas con explicación económica**, no indicadores: carry de funding (cobrar funding con cobertura delta-neutra),
   primas de riesgo como el momentum de serie temporal a varios meses, o market making con datos del libro. Todas exigen
   datos que hoy no tenemos.
3. **Tiempo**: 90 días de seguimiento hacia delante con PSR ≥ 0,95 antes de pensar en dinero real.
4. **S&P 500 y noticias** (tu petición): no he podido descargar datos (red bloqueada). Lo que se sabe de la literatura:
   el S&P 500 da de media ~8–10 % al año con Sharpe ~0,4–0,5. Las reglas de entrada y salida con indicadores rara vez
   le ganan a comprar y mantener después de costes. El análisis de noticias exige fuentes de pago y en minorista la
   evidencia es débil. Para probarlo en serio: descargar en el portátil 20 años de SPY diario y pasarlo por este mismo
   laboratorio. Es un mercado más eficiente que cripto, así que el listón es aún más alto.

## 6. Objetivo de Miguel (OBJETIVO.md). Detalle completo en `lab/objetivo_mc_4h.md`

### Lo que exige el objetivo
| Capital | +2.000 € en 5 meses | Equivale anual | Sharpe mínimo (con apalancamiento óptimo) para tener un 50 % de lograrlo |
|---|---|---|---|
| 1.000 € | +200 % | +1.297 % | 2,3 |
| 2.000 € | +100 % | +428 % | 1,8 |
| 5.000 € | +40 % | +124 % | 1,3 |
| 10.000 € | +20 % | +55 % | 0,9 |

Un Sharpe de 1 sostenido ya es excelente. Y, aun con el apalancamiento óptimo (Kelly), **la probabilidad de caer en algún
momento al 50 % del capital es del 50 %**: es una propiedad matemática de Kelly. Hoy no tenemos ninguna estrategia
con un Sharpe fuera de muestra demostrado mayor que 0.

### Probabilidades (Monte Carlo por bloques, 4.000 caminos de 5 meses, rentabilidades fuera de muestra, 4 h)
"Sin ventaja" = la misma serie con la media puesta a cero, que es lo que dice el SPA. "Con la de la reserva" = suponiendo
que se repite la racha de sept-oct, lo cual es optimista. Formato: **P(llegar a +2.000 €) / P(perder ≥ 50 %)**.

| Escenario | Apal. | 1.000 € | 2.000 € | 5.000 € | 10.000 € |
|---|---|---|---|---|---|
| Cartera de familias, sin ventaja | x1 | 0 % / 0 % | 0 % / 0 % | 1 % / 0 % | 10 % / 0 % |
| Cartera de familias, sin ventaja | x3 | 1 % / 17 % | 4 % / 17 % | 17 % / 17 % | 26 % / 17 % |
| Cartera de familias, sin ventaja | x5 | 4 % / 50 % | 10 % / 50 % | 21 % / 50 % | 27 % / 50 % |
| Cartera de familias, con la de la reserva | x3 | 2 % / 10 % | 9 % / 10 % | 29 % / 10 % | 41 % / 10 % |
| Cartera de familias, con la de la reserva | x5 | 8 % / 35 % | 20 % / 35 % | 33 % / 35 % | 41 % / 35 % |
| Comprar y mantener cripto, sin ventaja | x1 | 1 % / 18 % | 4 % / 18 % | 17 % / 18 % | 27 % / 18 % |
| Comprar y mantener cripto, sin ventaja | x2 | 5 % / 63 % | 11 % / 63 % | 20 % / 63 % | 25 % / 63 % |
| Comprar y mantener cripto, racha de sept-oct | x1 | 6 % / 3 % | 25 % / 3 % | 54 % / 3 % | 67 % / 3 % |

(Para +5.000 €, ver `lab/objetivo_mc_4h.md`: todo baja mucho.)

### Veredicto sin rodeos
- **Con 1.000 o 2.000 €, el objetivo es una lotería**: cada punto de probabilidad de lograrlo cuesta una probabilidad
  parecida o mayor de perder la mitad o más.
- **Con 10.000 €, +2.000 € (+20 %)** se puede conseguir si el mercado cripto sube, pero eso no es una estrategia
  sino exposición al mercado. Sin ventaja, la probabilidad ronda el 25 % con un riesgo de −50 % similar o mayor si se apalanca.
- **Objetivo realista** si algún día hay una estrategia validada con Sharpe ~1 y volatilidad del 20 %, sin apalancamiento:
  ~+8 % en 5 meses de media (≈ 800 € con 10.000 €), con una caída máxima típica del 10–15 %. Hoy ni eso está demostrado.
- No se ha operado nada real ni se han usado claves.
