#!/usr/bin/env bash
# Ejecucion completa en GitHub Actions (o cualquier Linux con red). Solo datos publicos, sin claves, sin ordenes.
# Para cada fuente de datos que se pueda descargar: laboratorio 4h y 1h, meta-validacion, SPA, carry y Monte Carlo.
# Deja todo en resultados/<fuente>/ y un resumen en resultados/RESUMEN.txt
set -u
cd "$(dirname "$0")"
export PYTHONUTF8=1
PRUEBAS="${PRUEBAS:-3000}"
RES=../resultados
mkdir -p "$RES"
: > "$RES/RESUMEN.txt"

echo "== Descargas ==" | tee -a "$RES/RESUMEN.txt"
timeout 150m python datos.py 1h 4h > "$RES/descarga_hyperliquid.log" 2>&1 \
  && echo "hyperliquid: ok" | tee -a "$RES/RESUMEN.txt" || echo "hyperliquid: FALLO (ver log)" | tee -a "$RES/RESUMEN.txt"
for ex in binanceusdm bybit okx; do
  timeout 60m python -m herramientas.descarga_ccxt --exchange $ex --desde 2022-01-01 > "$RES/descarga_$ex.log" 2>&1 \
    && { echo "$ex: ok" | tee -a "$RES/RESUMEN.txt"; break; } || echo "$ex: FALLO (ver log)" | tee -a "$RES/RESUMEN.txt"
done

for base in base.pkl.gz base_binanceusdm.pkl.gz base_bybit.pkl.gz base_okx.pkl.gz; do
  [ -s "datos/$base" ] || continue
  nombre="${base%.pkl.gz}"; dest="$RES/$nombre"; mkdir -p "$dest"
  export LAB_BASE=$base
  echo "== $base ==" | tee -a "$RES/RESUMEN.txt"
  rm -f registro_*.csv estado_*.json reserva_*.pkl
  for iv in 4h 1h; do
    python automejora.py --intervalo $iv --sin-descarga --pruebas "$PRUEBAS" > "$dest/salida_automejora_$iv.txt" 2>&1
    python meta_validacion.py --intervalo $iv > "$dest/salida_meta_$iv.txt" 2>&1
    python spa.py --intervalo $iv --max 1500 > "$dest/salida_spa_$iv.txt" 2>&1
    python objetivo_mc.py --intervalo $iv > "$dest/salida_mc_$iv.txt" 2>&1
    cp -f informe_$iv.txt spa_$iv.txt meta_validacion_$iv.txt objetivo_mc_$iv.md registro_$iv.csv "$dest/" 2>/dev/null
    head -3 "informe_$iv.txt" >> "$RES/RESUMEN.txt" 2>/dev/null
    sed -n 2,3p "spa_$iv.txt" >> "$RES/RESUMEN.txt" 2>/dev/null
  done
  python carry_funding.py --grandes > "$dest/carry_grandes.txt" 2>&1
  python carry_funding.py > "$dest/carry_todas.txt" 2>&1
  tail -1 "$dest/carry_grandes.txt" >> "$RES/RESUMEN.txt"
  python juntar_resultados.py > /dev/null 2>&1 && cp -f ../PEGAR_A_CLAUDE.txt "$dest/diagnostico.txt"
done
grep -l Traceback "$RES"/*/salida_*.txt >> "$RES/RESUMEN.txt" 2>/dev/null
echo "Terminado $(date -u)" >> "$RES/RESUMEN.txt"
