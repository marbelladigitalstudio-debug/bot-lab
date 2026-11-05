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

## Monte Carlo 1h (bootstrap estacionario, bloque medio 1 día, 4000 caminos, 3650 barras = 5 meses)
Reserva: 1500 barras (03/09/26 → 05/11/26). `mejor_busqueda` = cambio_regimen.

- **cartera_familias**: Sharpe reserva -1.37, rentab. anualizada -41%, vol anual 30%
- **mejor_busqueda**: Sharpe reserva -6.93, rentab. anualizada -193%, vol anual 28%
- **mercado**: Sharpe reserva +0.87, rentab. anualizada +59%, vol anual 68%

### Objetivo +2.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 1% / 0% | 3% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 33% | 0% / 33% | 3% / 33% | 6% / 33% |
| cartera_familias | la de la reserva | x3 | 0% / 65% | 2% / 65% | 4% / 65% | 7% / 65% |
| cartera_familias | la de la reserva | x5 | 1% / 87% | 3% / 87% | 5% / 87% | 6% / 87% |
| cartera_familias | la de la reserva | x10 | 1% / 99% | 2% / 99% | 3% / 99% | 3% / 99% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 4% / 0% | 15% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 9% | 3% / 9% | 15% / 9% | 25% / 9% |
| cartera_familias | cero (SPA) | x3 | 2% / 32% | 7% / 32% | 19% / 32% | 27% / 32% |
| cartera_familias | cero (SPA) | x5 | 5% / 64% | 12% / 64% | 20% / 64% | 25% / 64% |
| cartera_familias | cero (SPA) | x10 | 6% / 91% | 9% / 91% | 13% / 91% | 14% / 91% |
| mejor_busqueda | la de la reserva | x1 | 0% / 76% | 0% / 76% | 0% / 76% | 0% / 76% |
| mejor_busqueda | la de la reserva | x2 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x3 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x5 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x10 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 4% / 0% | 16% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 10% | 3% / 10% | 16% / 10% | 27% / 10% |
| mejor_busqueda | cero (SPA) | x3 | 2% / 30% | 8% / 30% | 22% / 30% | 29% / 30% |
| mejor_busqueda | cero (SPA) | x5 | 7% / 59% | 14% / 59% | 23% / 59% | 28% / 59% |
| mejor_busqueda | cero (SPA) | x10 | 9% / 89% | 13% / 89% | 17% / 89% | 19% / 89% |
| mercado | la de la reserva | x1 | 1% / 4% | 8% / 4% | 32% / 4% | 46% / 4% |
| mercado | la de la reserva | x2 | 11% / 34% | 23% / 34% | 39% / 34% | 46% / 34% |
| mercado | la de la reserva | x3 | 15% / 60% | 24% / 60% | 35% / 60% | 40% / 60% |
| mercado | la de la reserva | x5 | 12% / 87% | 17% / 87% | 22% / 87% | 24% / 87% |
| mercado | la de la reserva | x10 | 2% / 100% | 3% / 100% | 3% / 100% | 3% / 100% |
| mercado | cero (SPA) | x1 | 0% / 11% | 2% / 11% | 14% / 11% | 24% / 11% |
| mercado | cero (SPA) | x2 | 3% / 56% | 9% / 56% | 18% / 56% | 23% / 56% |
| mercado | cero (SPA) | x3 | 5% / 78% | 10% / 78% | 16% / 78% | 18% / 78% |
| mercado | cero (SPA) | x5 | 4% / 95% | 6% / 95% | 8% / 95% | 10% / 95% |
| mercado | cero (SPA) | x10 | 0% / 100% | 0% / 100% | 1% / 100% | 1% / 100% |

### Objetivo +5.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 33% | 0% / 33% | 0% / 33% | 2% / 33% |
| cartera_familias | la de la reserva | x3 | 0% / 65% | 0% / 65% | 2% / 65% | 4% / 65% |
| cartera_familias | la de la reserva | x5 | 0% / 87% | 1% / 87% | 3% / 87% | 4% / 87% |
| cartera_familias | la de la reserva | x10 | 0% / 99% | 1% / 99% | 2% / 99% | 3% / 99% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 2% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 9% | 0% / 9% | 3% / 9% | 11% / 9% |
| cartera_familias | cero (SPA) | x3 | 0% / 32% | 1% / 32% | 7% / 32% | 16% / 32% |
| cartera_familias | cero (SPA) | x5 | 2% / 64% | 4% / 64% | 12% / 64% | 19% / 64% |
| cartera_familias | cero (SPA) | x10 | 3% / 91% | 5% / 91% | 9% / 91% | 12% / 91% |
| mejor_busqueda | la de la reserva | x1 | 0% / 76% | 0% / 76% | 0% / 76% | 0% / 76% |
| mejor_busqueda | la de la reserva | x2 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x3 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x5 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | la de la reserva | x10 | 0% / 100% | 0% / 100% | 0% / 100% | 0% / 100% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 2% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 10% | 0% / 10% | 3% / 10% | 12% / 10% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 30% | 1% / 30% | 8% / 30% | 18% / 30% |
| mejor_busqueda | cero (SPA) | x5 | 1% / 59% | 5% / 59% | 14% / 59% | 21% / 59% |
| mejor_busqueda | cero (SPA) | x10 | 4% / 89% | 8% / 89% | 13% / 89% | 16% / 89% |
| mercado | la de la reserva | x1 | 0% / 4% | 0% / 4% | 8% / 4% | 26% / 4% |
| mercado | la de la reserva | x2 | 2% / 34% | 7% / 34% | 23% / 34% | 35% / 34% |
| mercado | la de la reserva | x3 | 5% / 60% | 12% / 60% | 24% / 60% | 32% / 60% |
| mercado | la de la reserva | x5 | 7% / 87% | 11% / 87% | 17% / 87% | 21% / 87% |
| mercado | la de la reserva | x10 | 1% / 100% | 2% / 100% | 3% / 100% | 3% / 100% |
| mercado | cero (SPA) | x1 | 0% / 11% | 0% / 11% | 2% / 11% | 10% / 11% |
| mercado | cero (SPA) | x2 | 0% / 56% | 2% / 56% | 9% / 56% | 16% / 56% |
| mercado | cero (SPA) | x3 | 1% / 78% | 4% / 78% | 10% / 78% | 14% / 78% |
| mercado | cero (SPA) | x5 | 2% / 95% | 3% / 95% | 6% / 95% | 8% / 95% |
| mercado | cero (SPA) | x10 | 0% / 100% | 0% / 100% | 0% / 100% | 1% / 100% |

