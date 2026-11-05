"""Herramientas opcionales del bot (datos, noticias, regimen, validacion, avisos). Ver LEEME.md."""
import os
import sys

_LAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _LAB not in sys.path:
    sys.path.insert(0, _LAB)


def requiere(modulo, archivo):
    """Importa una libreria opcional o explica como instalarla (version fijada)."""
    import importlib
    try:
        return importlib.import_module(modulo)
    except ImportError:
        raise SystemExit(f"Falta '{modulo}'. Instala con versiones fijas:  pip install -r requisitos/{archivo}")
