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
Reserva: 12701 barras (19/05/25 → 31/10/26). `mejor_busqueda` = rsi_reversion.

- **cartera_familias**: Sharpe reserva -0.20, rentab. anualizada -4%, vol anual 18%
- **mejor_busqueda**: Sharpe reserva -1.26, rentab. anualizada -11%, vol anual 9%
- **mercado**: Sharpe reserva -0.31, rentab. anualizada -19%, vol anual 62%

### Objetivo +2.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 5% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 6% / 0% | 16% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 8% | 2% / 8% | 12% / 8% | 21% / 8% |
| cartera_familias | la de la reserva | x5 | 2% / 37% | 6% / 37% | 17% / 37% | 24% / 37% |
| cartera_familias | la de la reserva | x10 | 5% / 78% | 10% / 78% | 16% / 78% | 20% / 78% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 6% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 7% / 0% | 19% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 6% | 2% / 6% | 14% / 6% | 25% / 6% |
| cartera_familias | cero (SPA) | x5 | 2% / 33% | 8% / 33% | 20% / 33% | 27% / 33% |
| cartera_familias | cero (SPA) | x10 | 7% / 74% | 12% / 74% | 20% / 74% | 23% / 74% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x3 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x5 | 0% / 6% | 0% / 6% | 0% / 6% | 2% / 6% |
| mejor_busqueda | la de la reserva | x10 | 0% / 54% | 0% / 54% | 2% / 54% | 4% / 54% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 0% | 0% / 0% | 0% / 0% | 7% / 0% |
| mejor_busqueda | cero (SPA) | x5 | 0% / 1% | 0% / 1% | 4% / 1% | 17% / 1% |
| mejor_busqueda | cero (SPA) | x10 | 0% / 23% | 2% / 23% | 15% / 23% | 23% / 23% |
| mercado | la de la reserva | x1 | 0% / 16% | 2% / 16% | 11% / 16% | 20% / 16% |
| mercado | la de la reserva | x2 | 2% / 60% | 7% / 60% | 16% / 60% | 20% / 60% |
| mercado | la de la reserva | x3 | 4% / 81% | 9% / 81% | 15% / 81% | 18% / 81% |
| mercado | la de la reserva | x5 | 4% / 94% | 6% / 94% | 9% / 94% | 10% / 94% |
| mercado | la de la reserva | x10 | 1% / 100% | 1% / 100% | 1% / 100% | 1% / 100% |
| mercado | cero (SPA) | x1 | 0% / 12% | 2% / 12% | 15% / 12% | 26% / 12% |
| mercado | cero (SPA) | x2 | 4% / 53% | 10% / 53% | 20% / 53% | 27% / 53% |
| mercado | cero (SPA) | x3 | 7% / 75% | 12% / 75% | 19% / 75% | 23% / 75% |
| mercado | cero (SPA) | x5 | 6% / 92% | 9% / 92% | 12% / 92% | 14% / 92% |
| mercado | cero (SPA) | x10 | 1% / 99% | 2% / 99% | 2% / 99% | 2% / 99% |

### Objetivo +5.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 3% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 8% | 0% / 8% | 2% / 8% | 9% / 8% |
| cartera_familias | la de la reserva | x5 | 0% / 37% | 1% / 37% | 6% / 37% | 14% / 37% |
| cartera_familias | la de la reserva | x10 | 2% / 78% | 4% / 78% | 10% / 78% | 15% / 78% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 4% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 6% | 0% / 6% | 2% / 6% | 10% / 6% |
| cartera_familias | cero (SPA) | x5 | 0% / 33% | 1% / 33% | 8% / 33% | 17% / 33% |
| cartera_familias | cero (SPA) | x10 | 2% / 74% | 5% / 74% | 12% / 74% | 18% / 74% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x3 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | la de la reserva | x5 | 0% / 6% | 0% / 6% | 0% / 6% | 0% / 6% |
| mejor_busqueda | la de la reserva | x10 | 0% / 54% | 0% / 54% | 0% / 54% | 1% / 54% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x5 | 0% / 1% | 0% / 1% | 0% / 1% | 2% / 1% |
| mejor_busqueda | cero (SPA) | x10 | 0% / 23% | 0% / 23% | 2% / 23% | 11% / 23% |
| mercado | la de la reserva | x1 | 0% / 16% | 0% / 16% | 2% / 16% | 8% / 16% |
| mercado | la de la reserva | x2 | 0% / 60% | 2% / 60% | 7% / 60% | 14% / 60% |
| mercado | la de la reserva | x3 | 1% / 81% | 3% / 81% | 9% / 81% | 13% / 81% |
| mercado | la de la reserva | x5 | 2% / 94% | 4% / 94% | 6% / 94% | 8% / 94% |
| mercado | la de la reserva | x10 | 0% / 100% | 1% / 100% | 1% / 100% | 1% / 100% |
| mercado | cero (SPA) | x1 | 0% / 12% | 0% / 12% | 2% / 12% | 11% / 12% |
| mercado | cero (SPA) | x2 | 0% / 53% | 2% / 53% | 10% / 53% | 18% / 53% |
| mercado | cero (SPA) | x3 | 2% / 75% | 5% / 75% | 12% / 75% | 18% / 75% |
| mercado | cero (SPA) | x5 | 3% / 92% | 6% / 92% | 9% / 92% | 12% / 92% |
| mercado | cero (SPA) | x10 | 1% / 99% | 1% / 99% | 2% / 99% | 2% / 99% |

