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
Reserva: 324 barras (02/09/26 → 26/10/26). `mejor_busqueda` = bollinger_reversion.

- **cartera_familias**: Sharpe reserva +0.63, rentab. anualizada +15%, vol anual 24%
- **mejor_busqueda**: Sharpe reserva +0.04, rentab. anualizada +1%, vol anual 21%
- **mercado**: Sharpe reserva +1.62, rentab. anualizada +119%, vol anual 74%

### Objetivo +2.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 4% / 0% | 20% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 1% | 3% / 1% | 21% / 1% | 36% / 1% |
| cartera_familias | la de la reserva | x3 | 2% / 10% | 9% / 10% | 29% / 10% | 41% / 10% |
| cartera_familias | la de la reserva | x5 | 8% / 35% | 20% / 35% | 33% / 35% | 41% / 35% |
| cartera_familias | la de la reserva | x10 | 14% / 74% | 21% / 74% | 28% / 74% | 31% / 74% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 1% / 0% | 10% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 3% | 1% / 3% | 11% / 3% | 23% / 3% |
| cartera_familias | cero (SPA) | x3 | 1% / 17% | 4% / 17% | 17% / 17% | 26% / 17% |
| cartera_familias | cero (SPA) | x5 | 4% / 50% | 10% / 50% | 21% / 50% | 27% / 50% |
| cartera_familias | cero (SPA) | x10 | 7% / 84% | 11% / 84% | 16% / 84% | 19% / 84% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 3% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 0% / 0% | 3% / 0% | 15% / 0% |
| mejor_busqueda | la de la reserva | x3 | 0% / 4% | 0% / 4% | 9% / 4% | 20% / 4% |
| mejor_busqueda | la de la reserva | x5 | 0% / 32% | 3% / 32% | 14% / 32% | 22% / 32% |
| mejor_busqueda | la de la reserva | x10 | 3% / 79% | 6% / 79% | 11% / 79% | 15% / 79% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 3% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 3% / 0% | 14% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 5% | 0% / 5% | 8% / 5% | 19% / 5% |
| mejor_busqueda | cero (SPA) | x5 | 0% / 33% | 3% / 33% | 13% / 33% | 21% / 33% |
| mejor_busqueda | cero (SPA) | x10 | 2% / 79% | 6% / 79% | 11% / 79% | 14% / 79% |
| mercado | la de la reserva | x1 | 6% / 3% | 25% / 3% | 54% / 3% | 67% / 3% |
| mercado | la de la reserva | x2 | 28% / 26% | 44% / 26% | 59% / 26% | 65% / 26% |
| mercado | la de la reserva | x3 | 33% / 50% | 44% / 50% | 54% / 50% | 58% / 50% |
| mercado | la de la reserva | x5 | 27% / 79% | 33% / 79% | 39% / 79% | 41% / 79% |
| mercado | la de la reserva | x10 | 6% / 99% | 7% / 99% | 8% / 99% | 8% / 99% |
| mercado | cero (SPA) | x1 | 1% / 18% | 4% / 18% | 17% / 18% | 27% / 18% |
| mercado | cero (SPA) | x2 | 5% / 63% | 11% / 63% | 20% / 63% | 25% / 63% |
| mercado | cero (SPA) | x3 | 7% / 81% | 11% / 81% | 16% / 81% | 20% / 81% |
| mercado | cero (SPA) | x5 | 5% / 95% | 7% / 95% | 9% / 95% | 10% / 95% |
| mercado | cero (SPA) | x10 | 1% / 100% | 1% / 100% | 1% / 100% | 1% / 100% |

### Objetivo +5.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 1% | 0% / 1% | 3% / 1% | 15% / 1% |
| cartera_familias | la de la reserva | x3 | 0% / 10% | 1% / 10% | 9% / 10% | 24% / 10% |
| cartera_familias | la de la reserva | x5 | 1% / 35% | 6% / 35% | 20% / 35% | 30% / 35% |
| cartera_familias | la de la reserva | x10 | 7% / 74% | 12% / 74% | 21% / 74% | 26% / 74% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 3% | 0% / 3% | 1% / 3% | 7% / 3% |
| cartera_familias | cero (SPA) | x3 | 0% / 17% | 0% / 17% | 4% / 17% | 14% / 17% |
| cartera_familias | cero (SPA) | x5 | 0% / 50% | 3% / 50% | 10% / 50% | 18% / 50% |
| cartera_familias | cero (SPA) | x10 | 3% / 84% | 6% / 84% | 11% / 84% | 15% / 84% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| mejor_busqueda | la de la reserva | x3 | 0% / 4% | 0% / 4% | 0% / 4% | 6% / 4% |
| mejor_busqueda | la de la reserva | x5 | 0% / 32% | 0% / 32% | 3% / 32% | 11% / 32% |
| mejor_busqueda | la de la reserva | x10 | 0% / 79% | 2% / 79% | 6% / 79% | 10% / 79% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 5% | 0% / 5% | 0% / 5% | 5% / 5% |
| mejor_busqueda | cero (SPA) | x5 | 0% / 33% | 0% / 33% | 3% / 33% | 10% / 33% |
| mejor_busqueda | cero (SPA) | x10 | 0% / 79% | 1% / 79% | 6% / 79% | 10% / 79% |
| mercado | la de la reserva | x1 | 0% / 3% | 4% / 3% | 25% / 3% | 47% / 3% |
| mercado | la de la reserva | x2 | 9% / 26% | 22% / 26% | 44% / 26% | 56% / 26% |
| mercado | la de la reserva | x3 | 17% / 50% | 29% / 50% | 44% / 50% | 52% / 50% |
| mercado | la de la reserva | x5 | 18% / 79% | 25% / 79% | 33% / 79% | 37% / 79% |
| mercado | la de la reserva | x10 | 4% / 99% | 5% / 99% | 7% / 99% | 7% / 99% |
| mercado | cero (SPA) | x1 | 0% / 18% | 0% / 18% | 4% / 18% | 14% / 18% |
| mercado | cero (SPA) | x2 | 1% / 63% | 4% / 63% | 11% / 63% | 18% / 63% |
| mercado | cero (SPA) | x3 | 3% / 81% | 6% / 81% | 11% / 81% | 15% / 81% |
| mercado | cero (SPA) | x5 | 3% / 95% | 5% / 95% | 7% / 95% | 9% / 95% |
| mercado | cero (SPA) | x10 | 0% / 100% | 0% / 100% | 1% / 100% | 1% / 100% |

