"""
LABORATORIO DE AUTOMEJORA
=========================
Cada ejecucion:
  1. Actualiza los datos (velas + funding de Hyperliquid, gratis).
  2. Prueba cientos de configuraciones nuevas de la biblioteca de estrategias:
     una parte al azar (explorar) y otra mutando las mejores que ya conoce (explotar),
     mas combinaciones de las mejores de familias distintas.
  3. Lo apunta TODO en registro_<intervalo>.csv. Las pruebas se acumulan entre dias,
     y por eso el listón sube solo: cuantas mas cosas prueba, mas exige (DSR).
  4. Pasa por los filtros a la mejor de cada familia:
        busqueda : DSR, estabilidad de parametros, PBO, numero de operaciones, concentracion
        reserva  : datos posteriores al corte que la busqueda NUNCA ve (con Bonferroni)
        adelante : rendimiento DESPUES del dia en que se eligio (la prueba de verdad)
  5. Escribe informe_<intervalo>.html, informe_<intervalo>.txt y senales_<intervalo>.txt.

Nunca opera con dinero real. "Promovida" significa: pasa a seguimiento en simulacion.

  python automejora.py                 (4h, descarga datos, 600 pruebas)
  python automejora.py --intervalo 1h
  python automejora.py --sin-descarga --pruebas 2000
"""
import argparse
import json
import os
import time
from itertools import combinations

import numpy as np
import pandas as pd

import comun as C
import datos
import estrategias as E
import motor
import validacion as V

COLS_REG = ["fecha", "familia", "clave", "params", "sr_barra", "sharpe", "n", "asim", "curt",
            "anual", "caida", "ops", "expo", "corr"]


# ------------------------------------------------------------------ utilidades
def _json_params(p):
    return json.dumps({k: (list(v) if isinstance(v, tuple) else v) for k, v in p.items()}, sort_keys=True)


def _params_json(s):
    d = json.loads(s)
    return {k: (tuple(v) if isinstance(v, list) else v) for k, v in d.items()}


def _ruta(nombre):
    return os.path.join(C.CARPETA, nombre)


def _leer_json(nombre, defecto):
    try:
        with open(_ruta(nombre), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return defecto


def _escribir_json(nombre, obj):
    with open(_ruta(nombre), "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False, default=str)


def fecha(ms):
    return pd.to_datetime(int(ms), unit="ms").strftime("%Y-%m-%d %H:%M")


class Lab:
    def __init__(self, iv, panel, pruebas, semilla):
        self.iv, self.panel, self.pruebas = iv, panel, pruebas
        self.rng = np.random.default_rng(semilla)
        self.idx = panel["close"].index.values
        self.estado = _leer_json(f"estado_{iv}.json", {})
        firma = f"{iv}|{int(self.idx[0])}|{panel.get('aproximado')}"
        if self.estado.get("firma") != firma or "corte" not in self.estado:
            if self.estado:
                print("AVISO: los datos cambiaron de origen. Empieza una generacion nueva (registro nuevo).")
            corte = int(self.idx[int(len(self.idx) * (1 - C.FRACCION_RESERVA))])
            self.estado = {"firma": firma, "corte": corte, "creado": time.strftime("%Y-%m-%d"),
                           "ejecuciones": [], "seguimiento": {}}
            if os.path.exists(_ruta(f"registro_{iv}.csv")):
                os.replace(_ruta(f"registro_{iv}.csv"), _ruta(f"registro_{iv}_anterior.csv"))
            _escribir_json(f"estado_{iv}.json", self.estado)
        self.corte = self.estado["corte"]
        n_busq = int((self.idx < self.corte).sum())
        cal = min(int(n_busq * 0.15), 60 * E.barras_dia(panel))
        self.ini = self.idx[cal]                      # calentamiento de indicadores
        self.m_busq = (self.idx >= self.ini) & (self.idx < self.corte)
        self.m_res = self.idx >= self.corte
        try:
            self.reg = pd.read_csv(_ruta(f"registro_{iv}.csv"))
        except (OSError, pd.errors.EmptyDataError):
            self.reg = pd.DataFrame(columns=COLS_REG)
        self.conocidas = set(self.reg["clave"])
        self.series = {}          # clave -> rentabilidad por barra en la busqueda (solo esta ejecucion)
        self.nuevas = []
        mercado = panel["close"].pct_change(fill_method=None).mean(axis=1).fillna(0.0)
        self.mercado = mercado

    # ---------------------------------------------------------- evaluar
    def pesos(self, fam, p):
        if fam == "conjunto":
            Ws = [self.pesos(*self._desde_clave(k)) for k in p["miembros"].split(";")]
            W = sum(w.reindex_like(self.panel["close"]).fillna(0.0) for w in Ws) / len(Ws)
            return W
        return E.FAMILIAS[fam]["fn"](self.panel, p)

    def _desde_clave(self, clave):
        fila = self.reg.loc[self.reg["clave"] == clave]
        if len(fila):
            return fila.iloc[0]["familia"], _params_json(fila.iloc[0]["params"])
        for n in self.nuevas:
            if n["clave"] == clave:
                return n["familia"], _params_json(n["params"])
        raise KeyError(clave)

    def evaluar(self, fam, p, contar=True):
        k = E.clave(fam, p) if fam != "conjunto" else "conjunto|" + p["miembros"]
        if k in self.series and (not contar or k in self.conocidas):
            return k
        W = self.pesos(fam, p)
        s = motor.simular(W, self.panel)
        rb = s["ret"][self.m_busq]
        m = motor.metricas(rb, self.iv, s["giro"][self.m_busq], s["exposicion"][self.m_busq])
        corr = float(np.corrcoef(rb, self.mercado[self.m_busq])[0, 1]) if rb.std() > 0 else 0.0
        self.series[k] = rb.values
        if contar and k not in self.conocidas:
            self.conocidas.add(k)
            self.nuevas.append({"fecha": time.strftime("%Y-%m-%d"), "familia": fam, "clave": k,
                                "params": _json_params(p), "sr_barra": m["sr_barra"], "sharpe": m["sharpe"],
                                "n": m["n"], "asim": m["asim"], "curt": m["curt"], "anual": m["anual"],
                                "caida": m["max_caida"], "ops": m["operaciones"], "expo": m["exposicion"],
                                "corr": corr})
        return k

    # ---------------------------------------------------------- generar candidatas
    def _azar(self, fam):
        return {k: v[self.rng.integers(len(v))] for k, v in E.FAMILIAS[fam]["espacio"].items()}

    def _mutar(self, fam, p):
        esp = E.FAMILIAS[fam]["espacio"]
        q = dict(p)
        for k in self.rng.choice(list(esp), size=min(2, len(esp)), replace=False):
            vals = esp[k]
            if k in q and q[k] in vals and len(vals) > 1:
                i = vals.index(q[k])
                j = int(np.clip(i + self.rng.choice([-1, 1]), 0, len(vals) - 1))
                q[k] = vals[j]
            else:
                q[k] = vals[self.rng.integers(len(vals))]
        return q

    def _validas(self, df):
        return df[(df["ops"] >= C.MIN_OPERACIONES) & (df["expo"] > 0.02)]

    def buscar(self):
        familias = list(E.FAMILIAS)
        presupuesto = self.pruebas
        hechas, intentos = 0, 0
        reg = self._validas(self.reg) if len(self.reg) else self.reg
        # explotar: mutaciones de las mejores conocidas (60 %) / explorar: azar (40 %)
        while hechas < presupuesto and intentos < presupuesto * 20:
            intentos += 1
            fam = familias[intentos % len(familias)]
            sub = reg[reg["familia"] == fam] if len(reg) else reg
            if len(sub) >= 5 and self.rng.random() < 0.6:
                top = sub.nlargest(5, "sharpe")
                base = _params_json(top.iloc[self.rng.integers(len(top))]["params"])
                p = self._mutar(fam, base)
            else:
                p = self._azar(fam)
            if E.clave(fam, p) in self.conocidas:
                continue
            try:
                self.evaluar(fam, p)
            except Exception as e:
                print(f"   fallo en {fam} {p}: {e}")
                continue
            hechas += 1
            if hechas % 100 == 0:
                print(f"   {hechas}/{presupuesto} pruebas")
        self._guardar_registro()
        print(f"   {hechas} configuraciones nuevas probadas (total historico: {len(self.reg)})")

    def conjuntos(self):
        """Combinaciones de la mejor de cada familia (senales debiles y poco correlacionadas)."""
        v = self._validas(self.reg[self.reg["familia"] != "conjunto"])
        if v.empty:
            return
        mejores = v.sort_values("sharpe", ascending=False).groupby("familia").head(1)
        mejores = mejores[mejores["sharpe"] > 0].head(6)
        claves = list(mejores["clave"])
        n = 0
        for r in (2, 3):
            for combo in combinations(claves, r):
                p = {"miembros": ";".join(combo)}
                if "conjunto|" + p["miembros"] in self.conocidas:
                    continue
                self.evaluar("conjunto", p)
                n += 1
        self._guardar_registro()
        print(f"   {n} combinaciones nuevas")

    def _guardar_registro(self):
        if self.nuevas:
            nuevo = pd.DataFrame(self.nuevas, columns=COLS_REG)
            self.reg = nuevo if self.reg.empty else pd.concat([self.reg, nuevo], ignore_index=True)
            for c in COLS_REG[4:]:
                self.reg[c] = pd.to_numeric(self.reg[c], errors="coerce")
            self.nuevas = []
            self.reg.to_csv(_ruta(f"registro_{self.iv}.csv"), index=False)

    # ---------------------------------------------------------- filtros
    def _serie(self, clave):
        if clave not in self.series:
            fam, p = self._desde_clave(clave)
            self.evaluar(fam, p, contar=False)
        return self.series[clave]

    def evaluar_candidatas(self):
        reg = self._validas(self.reg)
        n_total = len(self.reg)
        # N efectivo con las series de esta ejecucion
        if len(self.series) >= 10:
            M = np.column_stack(list(self.series.values()))
            ratio = V.n_efectivo(M) / M.shape[1]
        else:
            ratio = 0.3
        n_ef = max(1.0, n_total * ratio)
        var_sr = float(self.reg["sr_barra"].var()) if n_total > 2 else 0.0
        sr0 = V.sr_esperado_maximo(var_sr, n_ef)
        mejores = reg.sort_values("sharpe", ascending=False).groupby("familia").head(1)
        n_fam = max(1, len(mejores))
        umbral_res = 1 - (1 - C.PSR_RESERVA_MIN) / n_fam   # Bonferroni: se miran n_fam en la reserva
        filas = []
        for _, f in mejores.iterrows():
            fam, clave = f["familia"], f["clave"]
            p = _params_json(f["params"])
            W = self.pesos(fam, p)
            sim = motor.simular(W, self.panel)
            sim2 = motor.simular(W, self.panel, C.COSTE_LADO * 2)
            rb, rr = sim["ret"][self.m_busq], sim["ret"][self.m_res]
            mb = motor.metricas(rb, self.iv, sim["giro"][self.m_busq], sim["exposicion"][self.m_busq])
            mr = motor.metricas(rr, self.iv, sim["giro"][self.m_res], sim["exposicion"][self.m_res])
            mr2 = motor.metricas(sim2["ret"][self.m_res], self.iv)
            d = V.dsr(mb["sr_barra"], mb["n"], mb["asim"], mb["curt"], var_sr, n_ef)
            # estabilidad
            if fam == "conjunto":
                est = np.nan
            else:
                vs = []
                for q in E.vecinos(fam, p):
                    k = self.evaluar(fam, q)
                    s = self.series[k]
                    vs.append(s.mean() / s.std() if s.std() > 0 else 0.0)
                est = (np.median(vs) / mb["sr_barra"]) if vs and mb["sr_barra"] > 0 else 0.0
            # PBO de la familia: hasta 60 configuraciones conocidas
            sub = self.reg[self.reg["familia"] == fam].nlargest(60, "sharpe")
            M = np.column_stack([self._serie(k) for k in sub["clave"]]) if len(sub) >= 4 else None
            pb = V.pbo(M)[0] if M is not None else np.nan
            # concentracion en la busqueda
            Wl = motor.limpiar_pesos(W, self.panel).shift(1).fillna(0.0)
            r = self.panel["close"].pct_change(fill_method=None).fillna(0.0)
            pm = (Wl * r)[self.m_busq].sum()
            conc = float(pm.max() / pm[pm > 0].sum()) if (pm > 0).any() and pm.sum() > 0 else 1.0
            if len(E.universo(self.panel, p)) <= 1:
                conc = 0.0
            psr_r = V.psr(mr["sr_barra"], mr["n"], mr["asim"], mr["curt"])
            pasa = {
                "DSR": d >= C.DSR_MIN,
                "estable": fam == "conjunto" or est >= C.ESTABILIDAD_MIN,
                "PBO": not (pb == pb) or pb <= C.PBO_MAX,
                "concentr.": conc <= C.CONCENTRACION_MAX,
                "reserva": psr_r >= umbral_res and mr["anual"] > 0,
                "costes x2": mr2["anual"] > 0,
            }
            busqueda_ok = pasa["DSR"] and pasa["estable"] and pasa["PBO"] and pasa["concentr."]
            if all(pasa.values()):
                veredicto = "PROMOVIDA"
            elif busqueda_ok and mr["anual"] > 0:
                veredicto = "VIGILAR"
            else:
                veredicto = "DESCARTADA"
            filas.append({"familia": fam, "clave": clave, "fuente": E.FAMILIAS.get(fam, {}).get("fuente", "combinacion"),
                          "params": p, "busq": mb, "res": mr, "res_x2": mr2, "dsr": d, "estab": est,
                          "pbo": pb, "conc": conc, "psr_res": psr_r, "pasa": pasa, "veredicto": veredicto,
                          "ret": sim["ret"], "W": sim["W"], "corr": float(f["corr"])})
        self._guardar_registro()
        self.contexto = {"n_total": len(self.reg), "n_ef": n_ef, "sr0_anual": sr0 * np.sqrt(C.BARRAS_ANO[self.iv]),
                         "umbral_res": umbral_res, "n_fam": n_fam}
        return sorted(filas, key=lambda x: x["busq"]["sharpe"], reverse=True)

    # ---------------------------------------------------------- seguimiento hacia delante
    def seguimiento(self, filas):
        seg = self.estado.setdefault("seguimiento", {})
        ultimo = int(self.idx[-1])
        for f in filas:
            if f["veredicto"] in ("PROMOVIDA", "VIGILAR") and f["clave"] not in seg:
                seg[f["clave"]] = {"desde": ultimo, "familia": f["familia"], "veredicto": f["veredicto"],
                                   "params": _json_params(f["params"])}
            elif f["clave"] in seg:
                seg[f["clave"]]["veredicto"] = f["veredicto"]
        res = []
        for k, s in seg.items():
            fam, p = s["familia"], _params_json(s["params"])
            try:
                sim = motor.simular(self.pesos(fam, p), self.panel)
            except Exception:
                continue
            ra = sim["ret"][self.idx > s["desde"]]
            m = motor.metricas(ra, self.iv) if len(ra) >= 10 else None
            dias = len(ra) / E.barras_dia(self.panel)
            res.append({"clave": k, "familia": fam, "desde": s["desde"], "dias": dias,
                        "acum": float((1 + ra).prod() - 1) if len(ra) else 0.0,
                        "m": m, "psr": V.psr(m["sr_barra"], m["n"], m["asim"], m["curt"]) if m else 0.0,
                        "veredicto": s["veredicto"], "W_ultimo": sim["W"].iloc[-1]})
        return res


def referencias(lab):
    cl = lab.panel["close"]
    r = cl.pct_change(fill_method=None)
    out = {}
    if "BTC" in cl:
        out["Comprar y mantener BTC"] = r["BTC"].fillna(0.0)
    out["Cesta igual de todas (largo)"] = r.mean(axis=1).fillna(0.0)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--intervalo", default="4h", choices=["1h", "4h"])
    ap.add_argument("--pruebas", type=int, default=C.PRUEBAS_POR_EJECUCION)
    ap.add_argument("--sin-descarga", action="store_true")
    ap.add_argument("--semilla", type=int, default=C.SEMILLA)
    a = ap.parse_args()
    t0 = time.time()
    if not a.sin_descarga:
        try:
            datos.actualizar()
        except Exception as e:
            print(f"AVISO: no se pudieron actualizar los datos ({e}). Sigo con los guardados.")
    panel = datos.cargar(a.intervalo)
    print(f"Datos {a.intervalo}: {len(panel['close'])} barras, {panel['close'].shape[1]} monedas, "
          f"{fecha(panel['close'].index[0])} -> {fecha(panel['close'].index[-1])}")
    lab = Lab(a.intervalo, panel, a.pruebas, a.semilla)
    print(f"Busqueda: hasta {fecha(lab.corte)} | reserva (nunca vista al elegir): desde {fecha(lab.corte)}")
    print("1) Buscando configuraciones...")
    lab.buscar()
    print("2) Probando combinaciones...")
    lab.conjuntos()
    print("3) Pasando filtros...")
    filas = lab.evaluar_candidatas()
    seg = lab.seguimiento(filas)
    lab.estado["ejecuciones"].append({"fecha": time.strftime("%Y-%m-%d %H:%M"), "pruebas": lab.contexto["n_total"],
                                      "promovidas": sum(f["veredicto"] == "PROMOVIDA" for f in filas),
                                      "vigilar": sum(f["veredicto"] == "VIGILAR" for f in filas),
                                      "segundos": round(time.time() - t0)})
    _escribir_json(f"estado_{a.intervalo}.json", lab.estado)
    import informe
    informe.escribir(lab, filas, seg, referencias(lab))
    print(f"Hecho en {time.time() - t0:.0f} s. Abre lab\\informe_{a.intervalo}.html")


if __name__ == "__main__":
    main()
