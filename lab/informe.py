"""Informe HTML (se abre con doble clic) + resumen de texto para pegarselo a Claude."""
import html
import os
import time

import numpy as np
import pandas as pd

import comun as C

COLORES = ["#2563eb", "#d97706", "#059669", "#db2777", "#7c3aed"]


def _f(ms):
    return pd.to_datetime(int(ms), unit="ms").strftime("%d/%m/%y")


def _pct(x, d=1):
    return "—" if x is None or x != x else f"{x * 100:+.{d}f} %"


def _svg(series, corte, ancho=900, alto=300):
    """series: lista de (nombre, color, pd.Series de rentabilidad por barra). Curvas de capital (log)."""
    eqs = [(n, c, np.log((1 + s.fillna(0)).cumprod())) for n, c, s in series]
    idx = eqs[0][2].index.values
    x0, x1 = idx[0], idx[-1]
    ymin = min(float(e.min()) for _, _, e in eqs)
    ymax = max(float(e.max()) for _, _, e in eqs)
    if ymax - ymin < 1e-9:
        ymax = ymin + 1
    pad = 40

    def X(t):
        return pad + (t - x0) / (x1 - x0) * (ancho - 2 * pad)

    def Y(v):
        return alto - pad + (v - ymin) / (ymax - ymin) * (2 * pad - alto)

    partes = [f'<svg viewBox="0 0 {ancho} {alto}" role="img" class="grafico">']
    xc = X(corte)
    partes.append(f'<rect x="{xc:.1f}" y="{pad / 2}" width="{ancho - pad - xc:.1f}" height="{alto - 1.5 * pad}" class="zona"/>')
    partes.append(f'<text x="{xc + 6:.1f}" y="{pad / 2 + 14}" class="et">reserva (no vista al elegir)</text>')
    for v in np.linspace(ymin, ymax, 5):
        partes.append(f'<line x1="{pad}" x2="{ancho - pad}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" class="rej"/>')
        partes.append(f'<text x="{pad - 4}" y="{Y(v) + 4:.1f}" class="et" text-anchor="end">{(np.exp(v) - 1) * 100:+.0f}%</text>')
    for t in np.linspace(x0, x1, 5):
        partes.append(f'<text x="{X(t):.1f}" y="{alto - pad + 18}" class="et" text-anchor="middle">{_f(t)}</text>')
    paso = max(1, len(idx) // 600)
    for n, c, e in eqs:
        pts = " ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in zip(e.index.values[::paso], e.values[::paso]))
        discont = ' stroke-dasharray="4 3"' if n.startswith("Comprar") or n.startswith("Cesta") else ""
        partes.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="1.8"{discont}/>')
    partes.append("</svg>")
    ley = "".join(f'<span class="ley"><i style="background:{c}"></i>{html.escape(n)}</span>' for n, c, _ in series)
    return "".join(partes) + f'<div class="leyendas">{ley}</div>'


def _marca(ok):
    return '<span class="si">✔</span>' if ok else '<span class="no">✘</span>'


def escribir(lab, filas, seg, refs):
    iv = lab.iv
    ctx = lab.contexto
    n_p = sum(f["veredicto"] == "PROMOVIDA" for f in filas)
    n_v = sum(f["veredicto"] == "VIGILAR" for f in filas)
    ahora = time.strftime("%d/%m/%Y %H:%M")
    if n_p:
        titular = f"{n_p} estrategia(s) pasan todos los filtros y quedan en seguimiento en simulacion."
    elif n_v:
        titular = (f"Ninguna pasa todo. {n_v} pasan la busqueda y van positivas en la reserva, "
                   "pero sin suficiente evidencia: quedan en vigilancia.")
    else:
        titular = "Ninguna estrategia supera los filtros. Hoy no hay nada que merezca ni siquiera vigilancia."
    aviso = ('<p class="aviso">Datos aproximados (cache antigua de 180 dias, sin minimos ni volumen). '
             'Ejecuta datos.py para tener datos completos y mas historia.</p>') if lab.panel.get("aproximado") else ""

    filas_html = []
    for f in filas:
        b, r, r2, pz = f["busq"], f["res"], f["res_x2"], f["pasa"]
        est_s = "—" if f["estab"] != f["estab"] else f"{f['estab']:.2f}"
        pbo_s = "—" if f["pbo"] != f["pbo"] else f"{f['pbo']:.2f}"
        filas_html.append(
            f"<tr class='{f['veredicto'].lower()}'><td><b>{html.escape(f['familia'])}</b><br><small>{html.escape(f['fuente'])}</small></td>"
            f"<td>{b['sharpe']:.2f}</td><td>{f['dsr']:.2f} {_marca(pz['DSR'])}</td>"
            f"<td>{est_s} {_marca(pz['estable'])}</td>"
            f"<td>{pbo_s} {_marca(pz['PBO'])}</td>"
            f"<td>{f['conc']:.0%} {_marca(pz['concentr.'])}</td>"
            f"<td>{r['sharpe']:.2f}</td><td>{_pct(r['anual'])}</td><td>{f['psr_res']:.2f} {_marca(pz['reserva'])}</td>"
            f"<td>{_pct(r2['anual'])} {_marca(pz['costes x2'])}</td><td>{f['corr']:+.2f}</td>"
            f"<td><b>{f['veredicto']}</b></td></tr>")

    top = filas[:4]
    series = [(f"{f['familia']}", COLORES[i % 5], f["ret"][lab.idx >= lab.ini]) for i, f in enumerate(top)]
    for n, s in refs.items():
        series.append((n, "#9ca3af" if n.startswith("Comprar") else "#6b7280", s[lab.idx >= lab.ini]))
    grafico = _svg(series, lab.corte) if series else ""

    seg_html = []
    for s in sorted(seg, key=lambda x: -x["dias"]):
        m = s["m"]
        seg_html.append(f"<tr><td>{html.escape(s['familia'])}</td><td>{_f(s['desde'])}</td><td>{s['dias']:.0f}</td>"
                        f"<td>{_pct(s['acum'])}</td><td>{m['sharpe']:.2f}</td>" if m else
                        f"<tr><td>{html.escape(s['familia'])}</td><td>{_f(s['desde'])}</td><td>{s['dias']:.0f}</td>"
                        f"<td>{_pct(s['acum'])}</td><td>—</td>")
        seg_html[-1] += f"<td>{s['psr']:.2f}</td><td>{s['veredicto']}</td></tr>"

    sen = []
    for s in seg:
        w = s["W_ultimo"]
        w = w[w.abs() > 1e-4].sort_values()
        pos = ", ".join(f"{'LARGO' if v > 0 else 'CORTO'} {c} {abs(v):.0%}" for c, v in w.items()) or "sin posiciones (liquidez)"
        sen.append(f"{s['familia']}: {pos}")

    hist = "".join(f"<tr><td>{e['fecha']}</td><td>{e['pruebas']}</td><td>{e['promovidas']}</td><td>{e['vigilar']}</td>"
                   f"<td>{e['segundos']} s</td></tr>" for e in lab.estado.get("ejecuciones", [])[-15:][::-1])

    cuerpo = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Laboratorio {iv}</title>
<style>
:root{{--fondo:#f8fafc;--tarjeta:#fff;--texto:#0f172a;--suave:#64748b;--borde:#e2e8f0;--si:#059669;--no:#dc2626;--zona:#2563eb14}}
@media (prefers-color-scheme:dark){{:root{{--fondo:#0b1120;--tarjeta:#111827;--texto:#e5e7eb;--suave:#94a3b8;--borde:#1f2937;--zona:#60a5fa1f}}}}
body{{margin:0;background:var(--fondo);color:var(--texto);font:15px/1.5 system-ui,Segoe UI,sans-serif}}
main{{max-width:1100px;margin:0 auto;padding:24px 16px}}
h1{{font-size:24px;margin:0 0 4px}} h2{{font-size:17px;margin:28px 0 10px}}
.sub{{color:var(--suave)}} .tarjeta{{background:var(--tarjeta);border:1px solid var(--borde);border-radius:12px;padding:16px;margin:12px 0}}
.titular{{font-size:18px;font-weight:600}} .aviso{{color:#b45309}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px}}
.kpi b{{display:block;font-size:22px}} .kpi span{{color:var(--suave);font-size:13px}}
.tabla{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:13px}}
th,td{{padding:7px 8px;border-bottom:1px solid var(--borde);text-align:left;vertical-align:top;white-space:nowrap}}
th{{color:var(--suave);font-weight:600}} td small{{color:var(--suave);white-space:normal}}
.si{{color:var(--si)}} .no{{color:var(--no)}} tr.promovida td{{background:#05966914}} tr.vigilar td{{background:#d9770614}}
.grafico{{width:100%;height:auto}} .rej{{stroke:var(--borde)}} .et{{fill:var(--suave);font-size:11px}} .zona{{fill:var(--zona)}}
.leyendas{{display:flex;flex-wrap:wrap;gap:12px;font-size:13px}} .ley i{{display:inline-block;width:12px;height:3px;margin-right:6px;vertical-align:middle}}
li{{margin:4px 0}} code{{font-size:13px}}
</style></head><body><main>
<h1>Laboratorio de estrategias · {iv}</h1>
<div class="sub">Actualizado {ahora} · datos {_f(lab.idx[0])} → {_f(lab.idx[-1])} · {lab.panel['close'].shape[1]} monedas · solo simulación</div>
{aviso}
<div class="tarjeta"><div class="titular">{titular}</div>
<p class="sub">"Promovida" no significa dinero real: significa que pasa a la prueba hacia delante. Para plantearse dinero real hacen falta al menos 90 días hacia delante con PSR ≥ 0,95.</p></div>
<div class="kpis">
<div class="tarjeta kpi"><b>{ctx['n_total']:,}</b><span>configuraciones probadas (acumulado)</span></div>
<div class="tarjeta kpi"><b>{ctx['n_ef']:,.0f}</b><span>pruebas independientes estimadas</span></div>
<div class="tarjeta kpi"><b>{ctx['sr0_anual']:.2f}</b><span>Sharpe anual que saldría solo por azar</span></div>
<div class="tarjeta kpi"><b>{_f(lab.corte)}</b><span>inicio de la reserva</span></div>
</div>
<h2>La mejor de cada familia, filtro a filtro</h2>
<div class="tarjeta tabla"><table><tr><th>Familia</th><th>Sharpe búsq.</th><th>DSR ≥ {C.DSR_MIN}</th><th>Estable ≥ {C.ESTABILIDAD_MIN}</th>
<th>PBO ≤ {C.PBO_MAX}</th><th>Concentr.</th><th>Sharpe reserva</th><th>Anual reserva</th><th>PSR ≥ {ctx['umbral_res']:.3f}</th>
<th>Costes ×2</th><th>Corr. mercado</th><th>Veredicto</th></tr>{''.join(filas_html)}</table></div>
<h2>Curvas de capital (las 4 mejores en la búsqueda frente a comprar y mantener)</h2>
<div class="tarjeta">{grafico}</div>
<h2>Seguimiento hacia delante (después del día en que se eligieron)</h2>
<div class="tarjeta tabla"><table><tr><th>Familia</th><th>Desde</th><th>Días</th><th>Acumulado</th><th>Sharpe</th><th>PSR</th><th>Estado</th></tr>
{''.join(seg_html) or '<tr><td colspan=7>Todavía nada en seguimiento.</td></tr>'}</table></div>
<h2>Posiciones simuladas ahora</h2>
<div class="tarjeta"><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in sen) or '<li>Nada en seguimiento.</li>'}</ul></div>
<h2>Historial</h2>
<div class="tarjeta tabla"><table><tr><th>Ejecución</th><th>Pruebas acumuladas</th><th>Promovidas</th><th>Vigilar</th><th>Duración</th></tr>{hist}</table></div>
<h2>Cómo leer esto</h2>
<div class="tarjeta"><ul>
<li><b>Sharpe búsq.</b>: rentabilidad / riesgo en los datos usados para elegir. Siempre sale inflado.</li>
<li><b>DSR</b>: probabilidad de que ese Sharpe no sea suerte <i>teniendo en cuenta cuántas cosas se han probado</i>. Cuantas más pruebas acumula el laboratorio, más alto tiene que ser el Sharpe.</li>
<li><b>Estable</b>: si cambiar un poco los parámetros hunde el resultado, era casualidad.</li>
<li><b>PBO</b>: con qué frecuencia la mejor configuración de la familia acaba por debajo de la mediana en otro trozo de datos.</li>
<li><b>Reserva</b>: el último {C.FRACCION_RESERVA:.0%} de los datos, que la búsqueda nunca ve. Se exige más cuantas más familias se miran (corrección de Bonferroni).</li>
<li><b>Corr. mercado</b>: cerca de +1 = es casi comprar la cesta; la "ventaja" puede ser solo que el mercado subió.</li>
<li>Costes: {C.COSTE_LADO * 100:.3f} % por lado (comisión taker + deslizamiento) y funding real de cada hora.</li>
<li>Límites: monedas elegidas por su volumen de hoy (sesgo de supervivencia), sin stops intrabarra, un solo mercado.</li>
</ul></div>
</main></body></html>"""
    with open(os.path.join(C.CARPETA, f"informe_{iv}.html"), "w", encoding="utf-8") as fh:
        fh.write(cuerpo)

    # resumen de texto para pegar a Claude
    lin = [f"LABORATORIO {iv} — {ahora}", titular,
           f"Pruebas acumuladas {ctx['n_total']} (indep. ~{ctx['n_ef']:.0f}); Sharpe por azar ~{ctx['sr0_anual']:.2f}; "
           f"reserva desde {_f(lab.corte)}; umbral PSR reserva {ctx['umbral_res']:.3f}", "",
           "familia | sharpe_busq | DSR | estab | PBO | conc | sharpe_res | anual_res | PSR_res | anual_res_x2 | corr | veredicto"]
    for f in filas:
        lin.append(f"{f['familia']} | {f['busq']['sharpe']:.2f} | {f['dsr']:.2f} | "
                   f"{f['estab'] if f['estab'] != f['estab'] else round(f['estab'], 2)} | "
                   f"{f['pbo'] if f['pbo'] != f['pbo'] else round(f['pbo'], 2)} | {f['conc']:.0%} | "
                   f"{f['res']['sharpe']:.2f} | {_pct(f['res']['anual'])} | {f['psr_res']:.2f} | "
                   f"{_pct(f['res_x2']['anual'])} | {f['corr']:+.2f} | {f['veredicto']}")
        lin.append(f"    {f['clave']}")
    lin.append("")
    lin.append("SEGUIMIENTO HACIA DELANTE:")
    for s in seg:
        lin.append(f"  {s['familia']} desde {_f(s['desde'])}: {s['dias']:.0f} dias, {_pct(s['acum'])}, PSR {s['psr']:.2f}, {s['veredicto']}")
    lin.append("")
    lin += ["POSICIONES SIMULADAS AHORA:"] + [f"  {x}" for x in sen]
    with open(os.path.join(C.CARPETA, f"informe_{iv}.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lin) + "\n")
    with open(os.path.join(C.CARPETA, f"senales_{iv}.txt"), "w", encoding="utf-8") as fh:
        fh.write(f"Posiciones simuladas ({ahora})\n" + ("\n".join(sen) or "Nada en seguimiento.") + "\n")
