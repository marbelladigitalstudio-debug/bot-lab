"""
Noticias -> sentimiento por moneda y hora, SIN mirar el futuro.
  Fuentes: RSS publicos (feedparser, BSD-2) y GDELT DOC 2.0 (gdeltdoc, MIT; gratis, sin claves).
  Sentimiento: VADER (vaderSentiment, MIT) sobre titulares; rapido y sin descargar modelos.
  (Mejor calidad, mas pesado: FinBERT / FinGPT con transformers; ver referencias/HERRAMIENTAS.md.)
Los titulares se ACUMULAN en lab/datos/noticias.pkl.gz (los RSS solo dan los ultimos dias):
ejecutarlo a diario hace crecer el archivo, igual que datos.py.
Uso:  python -m herramientas.noticias            (descarga y guarda)
      senal = sentimiento_panel(panel)           (DataFrame tiempo x moneda para usar en una familia extra)
"""
import time

import numpy as np
import pandas as pd

from herramientas import requiere
import comun as C
import datos as D

FEEDS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss",
    "decrypt": "https://decrypt.co/feed",
    "theblock": "https://www.theblock.co/rss.xml",
    "yahoo_finanzas": "https://finance.yahoo.com/news/rssindex",
}
ALIAS = {"BTC": ["bitcoin", "btc"], "ETH": ["ethereum", "ether", "eth"], "SOL": ["solana"], "XRP": ["xrp", "ripple"],
         "DOGE": ["dogecoin", "doge"], "BNB": ["bnb", "binance coin"], "HYPE": ["hyperliquid"], "SUI": ["sui"],
         "ADA": ["cardano"], "LINK": ["chainlink"], "SPY": ["s&p 500", "s&p500", "wall street", "stocks"]}


def _analizador():
    m = requiere("vaderSentiment.vaderSentiment", "noticias.txt")
    return m.SentimentIntensityAnalyzer()


def leer_rss(feeds=FEEDS):
    fp = requiere("feedparser", "noticias.txt")
    filas = []
    for fuente, url in feeds.items():
        try:
            d = fp.parse(url)
        except Exception as e:
            print(f"  {fuente}: fallo {e}")
            continue
        for e in d.entries:
            t = e.get("published_parsed") or e.get("updated_parsed")
            if not t:
                continue
            filas.append({"t": int(time.mktime(t) * 1000), "fuente": fuente, "titulo": e.get("title", ""),
                          "url": e.get("link", "")})
    return pd.DataFrame(filas)


def leer_gdelt(consulta="bitcoin OR ethereum OR crypto", dias=7):
    g = requiere("gdeltdoc", "noticias.txt")
    f = g.Filters(keyword=consulta, timespan=f"{dias}d", language="english")
    arts = g.GdeltDoc().article_search(f)
    if arts is None or arts.empty:
        return pd.DataFrame(columns=["t", "fuente", "titulo", "url"])
    t = pd.to_datetime(arts["seendate"], format="%Y%m%dT%H%M%SZ", utc=True).astype("int64") // 10**6
    return pd.DataFrame({"t": t, "fuente": "gdelt:" + arts["domain"], "titulo": arts["title"], "url": arts["url"]})


def puntuar(df):
    an = _analizador()
    df = df.copy()
    df["sent"] = [an.polarity_scores(str(x))["compound"] for x in df["titulo"]]
    low = df["titulo"].str.lower()
    for m, alias in ALIAS.items():
        df[m] = low.apply(lambda s: any(a in s for a in alias))
    return df


def actualizar():
    viejo = D._leer("noticias.pkl.gz", pd.DataFrame())
    partes = [viejo]
    for f in (leer_rss, leer_gdelt):
        try:
            partes.append(f())
        except SystemExit:
            raise
        except Exception as e:
            print(f"  {f.__name__}: fallo ({e}); sigo")
    df = pd.concat([p for p in partes if len(p)], ignore_index=True)
    df = df.drop_duplicates(subset=["url", "titulo"]).sort_values("t")
    df = puntuar(df[["t", "fuente", "titulo", "url"]])
    D._escribir("noticias.pkl.gz", df)
    print(f"Noticias guardadas: {len(df)} titulares ({pd.to_datetime(df['t'].min(), unit='ms')} -> "
          f"{pd.to_datetime(df['t'].max(), unit='ms')})")
    return df


def sentimiento_panel(panel, df=None, retraso=1, ventana=24):
    """Sentimiento medio por moneda, asignado a la barra en cuyo CIERRE ya se conocia el titular,
    + 'retraso' barras de margen (las horas de publicacion a veces se corrigen despues). Media movil de 'ventana' barras."""
    df = D._leer("noticias.pkl.gz", None) if df is None else df
    idx = panel["close"].index
    cols = list(panel["close"].columns)
    out = pd.DataFrame(np.nan, index=idx, columns=cols)
    if df is None or not len(df):
        return out
    paso = C.MS_INTERVALO[panel["intervalo"]]
    barra = (df["t"] // paso) * paso + retraso * paso
    for m in cols:
        if m not in df:
            continue
        sel = df[m].astype(bool)
        s = df.loc[sel, "sent"].groupby(barra[sel]).mean()
        out[m] = s.reindex(idx)
    return out.rolling(ventana, min_periods=1).mean()


if __name__ == "__main__":
    actualizar()
