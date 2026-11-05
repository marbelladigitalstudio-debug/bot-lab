@echo off
REM ============================================================
REM  bot-lab: TODO EN UN DOBLE CLIC (solo simulacion, sin claves)
REM  1) instala lo necesario  2) baja 4 anos de datos publicos
REM  3) pasa todas las estrategias y filtros  4) abre el resultado
REM  Al final se abre PEGAR_A_CLAUDE.txt: copialo entero y pegalo en el chat.
REM ============================================================
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo No encuentro Python. Instalalo desde https://www.python.org/downloads/ marcando "Add python.exe to PATH" y vuelve a abrir este archivo.
  pause
  exit /b 1
)

echo.
echo [1/5] Instalando herramientas (versiones fijas)...
python -m pip install --disable-pip-version-check -q -r requisitos\datos.txt
if errorlevel 1 (
  echo Fallo al instalar. Copia lo que pone arriba y pegaselo a Claude.
  pause
  exit /b 1
)

cd lab
echo.
echo [2/5] Bajando datos desde 2022 (Binance; si falla, Bybit). Tarda 10-60 minutos...
set LAB_BASE=base_binanceusdm.pkl.gz
python -m herramientas.descarga_ccxt --exchange binanceusdm --desde 2022-01-01
if errorlevel 1 (
  echo Binance no responde; pruebo con Bybit...
  set LAB_BASE=base_bybit.pkl.gz
  python -m herramientas.descarga_ccxt --exchange bybit --desde 2022-01-01
  if errorlevel 1 (
    echo No he podido bajar datos de ningun exchange. Copia lo que pone arriba y pegaselo a Claude.
    pause
    exit /b 1
  )
)

echo.
echo [3/5] Probando estrategias con los filtros (unos 10-20 minutos)...
python automejora.py --intervalo 4h --sin-descarga --pruebas 3000 > salida_automejora.txt 2>&1
python meta_validacion.py --intervalo 4h > salida_meta.txt 2>&1

echo.
echo [4/5] Test SPA, carry de funding y Monte Carlo del objetivo...
python spa.py --intervalo 4h --max 1500 > salida_spa.txt 2>&1
python carry_funding.py --grandes > carry.txt 2>&1
python objetivo_mc.py --intervalo 4h > salida_mc.txt 2>&1

echo.
echo [5/5] Juntando resultados...
(
  echo ===== DATOS: %LAB_BASE% =====
  echo ===== INFORME 4h =====
  type informe_4h.txt
  echo.
  echo ===== SPA =====
  type spa_4h.txt
  echo.
  echo ===== CARRY DE FUNDING =====
  type carry.txt
  echo.
  echo ===== META-VALIDACION =====
  type meta_validacion_4h.txt
  echo.
  echo ===== MONTE CARLO OBJETIVO =====
  type objetivo_mc_4h.md
  echo.
  echo ===== ERRORES (si los hay) =====
  findstr /i "Traceback Error" salida_automejora.txt salida_meta.txt salida_spa.txt carry.txt salida_mc.txt
) > ..\PEGAR_A_CLAUDE.txt 2>&1

cd ..
echo.
echo LISTO. Se abre PEGAR_A_CLAUDE.txt: Ctrl+A, Ctrl+C y pegalo en el chat con Claude.
start notepad PEGAR_A_CLAUDE.txt
pause
