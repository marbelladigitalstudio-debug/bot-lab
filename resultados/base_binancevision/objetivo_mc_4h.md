# Traducción del objetivo

| Capital | Objetivo | Rentab. en 5 meses | Equivale anual | Sharpe mínimo (Kelly, 50 % de lograrlo) | Apalanc. Kelly si vol 60 %/año |
|---|---|---|---|---|---|
| 1.000 € | +2.000 € | +200% | +1297% | 2.3 | x3.8 |
| 2.000 € | +2.000 € | +100% | +428% | 1.8 | x3.0 |
| 5.000 € | +2.000 € | +40% | +124% | 1.3 | x2.1 |
| 10.000 € | +2.000 € | +20% | +55% | 0.9 | x1.6 |
| 1.000 € | +5.000 € | +500% | +7272% | 2.9 | x4.9 |
| 2.000 € | +5.000 € | +250% | +1922% | 2.5 | x4.1 |
| 5.000 € | +5.000 € | +100% | +428% | 1.8 | x3.0 |
| 10.000 € | +5.000 € | +50% | +165% | 1.4 | x2.3 |

## Monte Carlo 4h (bootstrap estacionario, bloque medio 1 día, 4000 caminos, 912 barras = 5 meses)
Reserva: 3176 barras (19/05/25 → 31/10/26). `mejor_busqueda` = macd_tendencia.

- **cartera_familias**: Sharpe reserva +0.23, rentab. anualizada +4%, vol anual 17%
- **mejor_busqueda**: Sharpe reserva +0.20, rentab. anualizada +5%, vol anual 26%
- **mercado**: Sharpe reserva -0.33, rentab. anualizada -20%, vol anual 61%

### Objetivo +2.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 7% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 8% / 0% | 22% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 5% | 3% / 5% | 15% / 5% | 28% / 5% |
| cartera_familias | la de la reserva | x5 | 3% / 25% | 9% / 25% | 23% / 25% | 32% / 25% |
| cartera_familias | la de la reserva | x10 | 9% / 66% | 15% / 66% | 23% / 66% | 28% / 66% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 6% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 6% / 0% | 18% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 6% | 2% / 6% | 13% / 6% | 23% / 6% |
| cartera_familias | cero (SPA) | x5 | 2% / 30% | 7% / 30% | 19% / 30% | 27% / 30% |
| cartera_familias | cero (SPA) | x10 | 7% / 71% | 12% / 71% | 19% / 71% | 23% / 71% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 4% / 0% | 16% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 5% | 3% / 5% | 16% / 5% | 27% / 5% |
| mejor_busqueda | la de la reserva | x3 | 2% / 21% | 9% / 21% | 22% / 21% | 30% / 21% |
| mejor_busqueda | la de la reserva | x5 | 7% / 50% | 14% / 50% | 25% / 50% | 30% / 50% |
| mejor_busqueda | la de la reserva | x10 | 10% / 84% | 14% / 84% | 19% / 84% | 21% / 84% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 3% / 0% | 13% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 7% | 2% / 7% | 13% / 7% | 24% / 7% |
| mejor_busqueda | cero (SPA) | x3 | 2% / 25% | 8% / 25% | 18% / 25% | 27% / 25% |
| mejor_busqueda | cero (SPA) | x5 | 6% / 55% | 12% / 55% | 21% / 55% | 26% / 55% |
| mejor_busqueda | cero (SPA) | x10 | 8% / 86% | 12% / 86% | 16% / 86% | 18% / 86% |
| mercado | la de la reserva | x1 | 0% / 15% | 1% / 15% | 10% / 15% | 20% / 15% |
| mercado | la de la reserva | x2 | 2% / 59% | 7% / 59% | 15% / 59% | 20% / 59% |
| mercado | la de la reserva | x3 | 4% / 79% | 8% / 79% | 14% / 79% | 17% / 79% |
| mercado | la de la reserva | x5 | 4% / 94% | 6% / 94% | 9% / 94% | 10% / 94% |
| mercado | la de la reserva | x10 | 1% / 100% | 1% / 100% | 1% / 100% | 1% / 100% |
| mercado | cero (SPA) | x1 | 0% / 11% | 2% / 11% | 15% / 11% | 26% / 11% |
| mercado | cero (SPA) | x2 | 4% / 51% | 10% / 51% | 21% / 51% | 27% / 51% |
| mercado | cero (SPA) | x3 | 7% / 73% | 12% / 73% | 19% / 73% | 23% / 73% |
| mercado | cero (SPA) | x5 | 6% / 91% | 9% / 91% | 12% / 91% | 14% / 91% |
| mercado | cero (SPA) | x10 | 1% / 99% | 2% / 99% | 2% / 99% | 2% / 99% |

### Objetivo +5.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 5% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 5% | 0% / 5% | 3% / 5% | 12% / 5% |
| cartera_familias | la de la reserva | x5 | 0% / 25% | 1% / 25% | 9% / 25% | 20% / 25% |
| cartera_familias | la de la reserva | x10 | 3% / 66% | 7% / 66% | 15% / 66% | 21% / 66% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 4% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 6% | 0% / 6% | 2% / 6% | 9% / 6% |
| cartera_familias | cero (SPA) | x5 | 0% / 30% | 1% / 30% | 7% / 30% | 16% / 30% |
| cartera_familias | cero (SPA) | x10 | 2% / 71% | 5% / 71% | 12% / 71% | 18% / 71% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 2% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 5% | 0% / 5% | 3% / 5% | 12% / 5% |
| mejor_busqueda | la de la reserva | x3 | 0% / 21% | 1% / 21% | 9% / 21% | 18% / 21% |
| mejor_busqueda | la de la reserva | x5 | 2% / 50% | 5% / 50% | 14% / 50% | 22% / 50% |
| mejor_busqueda | la de la reserva | x10 | 5% / 84% | 9% / 84% | 14% / 84% | 17% / 84% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 7% | 0% / 7% | 2% / 7% | 10% / 7% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 25% | 1% / 25% | 8% / 25% | 15% / 25% |
| mejor_busqueda | cero (SPA) | x5 | 1% / 55% | 4% / 55% | 12% / 55% | 19% / 55% |
| mejor_busqueda | cero (SPA) | x10 | 4% / 86% | 7% / 86% | 12% / 86% | 15% / 86% |
| mercado | la de la reserva | x1 | 0% / 15% | 0% / 15% | 1% / 15% | 8% / 15% |
| mercado | la de la reserva | x2 | 0% / 59% | 1% / 59% | 7% / 59% | 13% / 59% |
| mercado | la de la reserva | x3 | 1% / 79% | 3% / 79% | 8% / 79% | 13% / 79% |
| mercado | la de la reserva | x5 | 2% / 94% | 3% / 94% | 6% / 94% | 8% / 94% |
| mercado | la de la reserva | x10 | 1% / 100% | 1% / 100% | 1% / 100% | 1% / 100% |
| mercado | cero (SPA) | x1 | 0% / 11% | 0% / 11% | 2% / 11% | 11% / 11% |
| mercado | cero (SPA) | x2 | 0% / 51% | 2% / 51% | 10% / 51% | 19% / 51% |
| mercado | cero (SPA) | x3 | 2% / 73% | 5% / 73% | 12% / 73% | 18% / 73% |
| mercado | cero (SPA) | x5 | 3% / 91% | 5% / 91% | 9% / 91% | 11% / 91% |
| mercado | cero (SPA) | x10 | 1% / 99% | 1% / 99% | 2% / 99% | 2% / 99% |

