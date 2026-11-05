@echo off
REM Solo junta lo que ya hay (no descarga nada) y abre PEGAR_A_CLAUDE.txt con diagnostico.
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0lab"
if exist datos\base_bybit.pkl.gz set LAB_BASE=base_bybit.pkl.gz
if exist datos\base_binanceusdm.pkl.gz set LAB_BASE=base_binanceusdm.pkl.gz
python juntar_resultados.py
cd ..
start notepad PEGAR_A_CLAUDE.txt
pause
