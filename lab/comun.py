"""
Ajustes comunes del laboratorio. Todo lo editable esta aqui.
"""
import os
import time

CARPETA = os.path.dirname(os.path.abspath(__file__))
CARPETA_DATOS = os.path.join(CARPETA, "datos")
os.makedirs(CARPETA_DATOS, exist_ok=True)

API_INFO = "https://api.hyperliquid.xyz/info"
H = 3_600_000
MS_INTERVALO = {"1h": H, "4h": 4 * H, "1d": 24 * H}
BARRAS_ANO = {"1h": 8760, "4h": 2190, "1d": 365}

# --- costes (Hyperliquid, nivel base) ---
COMISION = 0.00045     # taker por lado
DESLIZAMIENTO = 0.0003  # estimado por lado (mas en monedas pequenas)
COSTE_LADO = COMISION + DESLIZAMIENTO   # por unidad de notional movido

# --- descarga ---
TOP_MONEDAS = 30        # por volumen de hoy; las que ya estan guardadas se siguen actualizando
PAUSA = 0.35

# --- validacion (filtros que tiene que pasar una estrategia) ---
FRACCION_RESERVA = 0.30   # el ultimo 30 % de los datos NUNCA se usa para elegir
DSR_MIN = 0.95            # Deflated Sharpe Ratio en la busqueda (corrige por nº de pruebas)
PSR_RESERVA_MIN = 0.90    # probabilidad de Sharpe > 0 en la reserva
ESTABILIDAD_MIN = 0.50    # los parametros vecinos deben conservar >= 50 % del Sharpe
CONCENTRACION_MAX = 0.50  # ninguna moneda puede aportar mas del 50 % del beneficio
PBO_MAX = 0.50            # probabilidad de sobreajuste de la familia (CSCV)
MIN_OPERACIONES = 30      # cambios de posicion en la busqueda

# --- bucle de automejora ---
PRUEBAS_POR_EJECUCION = 600
SEMILLA = None            # None = distinta cada dia (explora mas); un numero = repetible

# Universo "grandes" (se cruza con las monedas disponibles)
GRANDES = ["BTC", "ETH", "SOL", "XRP", "DOGE", "BNB", "HYPE", "SUI", "ADA", "LINK"]


def info(cuerpo, intentos=5):
    """Llamada a la API publica de Hyperliquid con reintentos."""
    import requests
    espera = 5
    for intento in range(intentos):
        try:
            r = requests.post(API_INFO, json=cuerpo, timeout=30)
        except requests.RequestException as e:
            if intento == intentos - 1:
                raise
            print(f"    (error de red: {e}; reintento en {espera} s)")
            time.sleep(espera)
            espera *= 2
            continue
        if r.status_code in (429, 500, 502, 503) and intento < intentos - 1:
            print(f"    (limite de la API o fallo {r.status_code}: espero {espera} s)")
            time.sleep(espera)
            espera *= 2
            continue
        r.raise_for_status()
        datos = r.json()
        # Hyperliquid limita a 1200 de "peso" por minuto: 20 por llamada + 1 por cada 20 filas de
        # funding o 60 velas. Se espera lo justo para quedar por debajo (~1000/min).
        n = len(datos) if isinstance(datos, list) else 0
        por = {"fundingHistory": 20, "candleSnapshot": 60}.get(cuerpo.get("type"), 0)
        peso = 20 + (n / por if por else 0)
        time.sleep(max(PAUSA, peso / 17))
        return datos
