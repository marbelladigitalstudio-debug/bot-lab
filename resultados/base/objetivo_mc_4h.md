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
Reserva: 1500 barras (28/02/26 → 05/11/26). `mejor_busqueda` = keltner_ruptura.

- **cartera_familias**: Sharpe reserva +0.34, rentab. anualizada +6%, vol anual 16%
- **mejor_busqueda**: Sharpe reserva +1.45, rentab. anualizada +22%, vol anual 15%
- **mercado**: Sharpe reserva +1.59, rentab. anualizada +98%, vol anual 62%

### Objetivo +2.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 1% / 0% | 8% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 9% / 0% | 23% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 2% | 3% / 2% | 17% / 2% | 29% / 2% |
| cartera_familias | la de la reserva | x5 | 3% / 20% | 10% / 20% | 25% / 20% | 34% / 20% |
| cartera_familias | la de la reserva | x10 | 10% / 61% | 17% / 61% | 26% / 61% | 31% / 61% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 6% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 6% / 0% | 18% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 4% | 2% / 4% | 12% / 4% | 23% / 4% |
| cartera_familias | cero (SPA) | x5 | 2% / 26% | 7% / 26% | 19% / 26% | 26% / 26% |
| cartera_familias | cero (SPA) | x10 | 7% / 69% | 12% / 69% | 20% / 69% | 24% / 69% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 3% / 0% | 20% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 3% / 0% | 21% / 0% | 43% / 0% |
| mejor_busqueda | la de la reserva | x3 | 2% / 0% | 10% / 0% | 34% / 0% | 52% / 0% |
| mejor_busqueda | la de la reserva | x5 | 10% / 3% | 24% / 3% | 46% / 3% | 58% / 3% |
| mejor_busqueda | la de la reserva | x10 | 25% / 29% | 38% / 29% | 51% / 29% | 57% / 29% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 1% / 0% | 7% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 1% / 0% | 8% / 0% | 18% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 1% / 2% | 3% / 2% | 14% / 2% | 23% / 2% |
| mejor_busqueda | cero (SPA) | x5 | 3% / 22% | 9% / 22% | 20% / 22% | 26% / 22% |
| mejor_busqueda | cero (SPA) | x10 | 8% / 65% | 14% / 65% | 21% / 65% | 24% / 65% |
| mercado | la de la reserva | x1 | 2% / 1% | 17% / 1% | 47% / 1% | 64% / 1% |
| mercado | la de la reserva | x2 | 21% / 18% | 38% / 18% | 57% / 18% | 66% / 18% |
| mercado | la de la reserva | x3 | 29% / 40% | 42% / 40% | 55% / 40% | 61% / 40% |
| mercado | la de la reserva | x5 | 28% / 69% | 36% / 69% | 42% / 69% | 46% / 69% |
| mercado | la de la reserva | x10 | 9% / 96% | 11% / 96% | 13% / 96% | 14% / 96% |
| mercado | cero (SPA) | x1 | 0% / 10% | 2% / 10% | 14% / 10% | 23% / 10% |
| mercado | cero (SPA) | x2 | 3% / 50% | 10% / 50% | 19% / 50% | 24% / 50% |
| mercado | cero (SPA) | x3 | 6% / 74% | 11% / 74% | 18% / 74% | 21% / 74% |
| mercado | cero (SPA) | x5 | 6% / 91% | 9% / 91% | 12% / 91% | 13% / 91% |
| mercado | cero (SPA) | x10 | 1% / 100% | 1% / 100% | 2% / 100% | 2% / 100% |

### Objetivo +5.000 € en 5 meses

| Candidata | Ventaja | Apal. | 1.000 €: P(obj) / P(−50 %) | 2.000 €: P(obj) / P(−50 %) | 5.000 €: P(obj) / P(−50 %) | 10.000 €: P(obj) / P(−50 %) |
|---|---|---|---|---|---|---|
| cartera_familias | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | la de la reserva | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 5% / 0% |
| cartera_familias | la de la reserva | x3 | 0% / 2% | 0% / 2% | 3% / 2% | 12% / 2% |
| cartera_familias | la de la reserva | x5 | 0% / 20% | 2% / 20% | 10% / 20% | 21% / 20% |
| cartera_familias | la de la reserva | x10 | 3% / 61% | 8% / 61% | 17% / 61% | 24% / 61% |
| cartera_familias | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| cartera_familias | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 0% / 0% | 4% / 0% |
| cartera_familias | cero (SPA) | x3 | 0% / 4% | 0% / 4% | 2% / 4% | 9% / 4% |
| cartera_familias | cero (SPA) | x5 | 0% / 26% | 1% / 26% | 7% / 26% | 16% / 26% |
| cartera_familias | cero (SPA) | x10 | 2% / 69% | 6% / 69% | 12% / 69% | 18% / 69% |
| mejor_busqueda | la de la reserva | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 1% / 0% |
| mejor_busqueda | la de la reserva | x2 | 0% / 0% | 0% / 0% | 3% / 0% | 15% / 0% |
| mejor_busqueda | la de la reserva | x3 | 0% / 0% | 1% / 0% | 10% / 0% | 28% / 0% |
| mejor_busqueda | la de la reserva | x5 | 1% / 3% | 7% / 3% | 24% / 3% | 42% / 3% |
| mejor_busqueda | la de la reserva | x10 | 12% / 29% | 21% / 29% | 38% / 29% | 49% / 29% |
| mejor_busqueda | cero (SPA) | x1 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% |
| mejor_busqueda | cero (SPA) | x2 | 0% / 0% | 0% / 0% | 1% / 0% | 5% / 0% |
| mejor_busqueda | cero (SPA) | x3 | 0% / 2% | 0% / 2% | 3% / 2% | 11% / 2% |
| mejor_busqueda | cero (SPA) | x5 | 0% / 22% | 2% / 22% | 9% / 22% | 17% / 22% |
| mejor_busqueda | cero (SPA) | x10 | 3% / 65% | 7% / 65% | 14% / 65% | 19% / 65% |
| mercado | la de la reserva | x1 | 0% / 1% | 1% / 1% | 17% / 1% | 40% / 1% |
| mercado | la de la reserva | x2 | 5% / 18% | 16% / 18% | 38% / 18% | 54% / 18% |
| mercado | la de la reserva | x3 | 13% / 40% | 25% / 40% | 42% / 40% | 52% / 40% |
| mercado | la de la reserva | x5 | 18% / 69% | 26% / 69% | 36% / 69% | 41% / 69% |
| mercado | la de la reserva | x10 | 7% / 96% | 9% / 96% | 11% / 96% | 13% / 96% |
| mercado | cero (SPA) | x1 | 0% / 10% | 0% / 10% | 2% / 10% | 11% / 10% |
| mercado | cero (SPA) | x2 | 0% / 50% | 2% / 50% | 10% / 50% | 17% / 50% |
| mercado | cero (SPA) | x3 | 2% / 74% | 5% / 74% | 11% / 74% | 16% / 74% |
| mercado | cero (SPA) | x5 | 3% / 91% | 5% / 91% | 9% / 91% | 11% / 91% |
| mercado | cero (SPA) | x10 | 1% / 100% | 1% / 100% | 1% / 100% | 2% / 100% |

