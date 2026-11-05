"""
Avisos (Telegram, correo, Discord...) con apprise (BSD-2). NO se guardan claves en el repo:
la direccion se lee de la variable de entorno BOT_AVISOS, p. ej.  tgram://<token>/<chat_id>  (ver docs de apprise).
Uso:  python -m herramientas.avisos "texto"    o   avisar(texto) desde el laboratorio.
"""
import os
import sys

from herramientas import requiere


def avisar(texto, titulo="bot-lab"):
    url = os.environ.get("BOT_AVISOS")
    if not url:
        print(f"[aviso sin enviar: define BOT_AVISOS] {titulo}: {texto}")
        return False
    apprise = requiere("apprise", "avisos.txt")
    a = apprise.Apprise()
    a.add(url)
    return a.notify(body=texto, title=titulo)


if __name__ == "__main__":
    avisar(" ".join(sys.argv[1:]) or "prueba")
