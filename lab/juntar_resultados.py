"""
Junta resultados + diagnostico en PEGAR_A_CLAUDE.txt (carpeta principal), aunque algun paso haya fallado.
Uso: python juntar_resultados.py      (lo llaman HAZLO_TODO.bat y VER_RESULTADOS.bat)
"""
import glob
import gzip
import os
import pickle
import platform
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(os.path.dirname(AQUI), "PEGAR_A_CLAUDE.txt")
ARCHIVOS = ["informe_4h.txt", "spa_4h.txt", "carry.txt", "meta_validacion_4h.txt", "objetivo_mc_4h.md"]


def leer(ruta, ultimas=None):
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            with open(ruta, encoding=enc) as f:
                lineas = f.read().splitlines()
            break
        except UnicodeDecodeError:
            continue
    if ultimas:
        lineas = lineas[-ultimas:]
    return "\n".join(lineas)


def edad(ruta):
    horas = (time.time() - os.path.getmtime(ruta)) / 3600
    return f"modificado hace {horas:.1f} h" + ("  <-- ANTIGUO (no es de esta ejecucion)" if horas > 12 else "")


def main():
    out = ["===== DIAGNOSTICO =====",
           f"Python {sys.version.split()[0]} en {platform.platform()}",
           f"Carpeta: {AQUI}",
           f"LAB_BASE = {os.environ.get('LAB_BASE', '(sin definir)')}"]
    for mod in ("numpy", "pandas", "ccxt", "requests"):
        try:
            m = __import__(mod)
            out.append(f"  {mod} {getattr(m, '__version__', '?')}")
        except Exception as e:
            out.append(f"  {mod} NO INSTALADO ({e.__class__.__name__})")
    out.append("Datos descargados (lab/datos):")
    for ruta in sorted(glob.glob(os.path.join(AQUI, "datos", "*.pkl.gz"))):
        linea = f"  {os.path.basename(ruta)}: {os.path.getsize(ruta) / 1e6:.1f} MB, {edad(ruta)}"
        try:
            with gzip.open(ruta, "rb") as f:
                b = pickle.load(f)
            if isinstance(b, dict) and "velas" in b:
                for iv, v in b["velas"].items():
                    ts = [t for c in v.values() for t in c]
                    if ts:
                        linea += (f"\n     {iv}: {len(v)} monedas, {time.strftime('%Y-%m-%d', time.gmtime(min(ts) / 1000))}"
                                  f" -> {time.strftime('%Y-%m-%d', time.gmtime(max(ts) / 1000))}")
        except Exception as e:
            linea += f" (no se puede leer: {e})"
        out.append(linea)
    if len(out) and out[-1] == "Datos descargados (lab/datos):":
        out.append("  NINGUNO: la descarga no llego a guardar nada")
    for nombre in ARCHIVOS:
        ruta = os.path.join(AQUI, nombre)
        out.append(f"\n===== {nombre} =====")
        out.append(f"({edad(ruta)})\n" + leer(ruta) if os.path.exists(ruta) else "NO EXISTE")
    for ruta in sorted(glob.glob(os.path.join(AQUI, "salida_*.txt"))):
        out.append(f"\n===== ultimas lineas de {os.path.basename(ruta)} ({edad(ruta)}) =====")
        out.append(leer(ruta, ultimas=25))
    with open(SALIDA, "w", encoding="utf-8-sig") as f:
        f.write("\n".join(out) + "\n")
    print("Resultados en", SALIDA)


if __name__ == "__main__":
    main()
