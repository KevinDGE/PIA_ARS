# -*- coding: utf-8 -*-
"""Genera el guion de la presentación en PDF (con miniatura de cada diapositiva)
a partir de src/guion.py. Requiere que el PowerPoint ya esté generado."""
import glob
import html
import os
import shutil
import subprocess
import sys

import data as D
import guion as G
from build_doc import BUILD, OUT, img_data_uri, render_pdf, stamp

e = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
PPTX = os.path.join(OUT, "Presentacion_Ejecutiva_Casino_Royale.pptx")
FINAL = os.path.join(OUT, "Guion_Presentacion_Ejecutiva.pdf")


def miniaturas():
    d = os.path.join(BUILD, "miniaturas")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    shutil.copy(PPTX, os.path.join(d, "p.pptx"))
    soffice = os.path.join(os.environ["PPTX_SKILL"], "scripts", "office", "soffice.py")
    subprocess.run([sys.executable, soffice, "--headless", "--convert-to", "pdf", "p.pptx"], cwd=d, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=240)
    subprocess.run(["pdftoppm", "-jpeg", "-r", "60", "p.pdf", "s"], cwd=d, check=True)
    files = sorted(glob.glob(os.path.join(d, "s-*.jpg")))
    if len(files) != len(G.DIAPOSITIVAS):
        sys.exit(f"Se esperaban {len(G.DIAPOSITIVAS)} miniaturas y hay {len(files)}")
    return files


def fmt_min(m):
    s = round(m * 60 / 15) * 15
    return f"{s // 60}:{s % 60:02d} min"


def build_html(thumbs):
    total_pal = sum(G.palabras(d) for d in G.DIAPOSITIVAS)
    reparto = ""
    for k, (quien, tema, ss) in enumerate(G.PARTES, start=1):
        pal = sum(G.palabras(G.DIAPOSITIVAS[n - 1]) for n in ss)
        rango = f"{ss[0]}–{ss[-1]}" if len(ss) > 1 else str(ss[0])
        reparto += (f"<tr><td class='c'><b>{k}</b></td><td><b>{e(G.ORADORES[quien])}</b></td><td>{e(tema)}</td>"
                    f"<td class='c nw'>{rango}</td><td class='c nw'>{fmt_min(G.minutos(pal))}</td></tr>")
    reparto += (f"<tr class='tot'><td></td><td colspan='3'><b>Total</b></td>"
                f"<td class='c nw'><b>{fmt_min(G.minutos(total_pal))}</b></td></tr>")

    partes = []
    for k, (quien, tema, ss) in enumerate(G.PARTES, start=1):
        pal = sum(G.palabras(G.DIAPOSITIVAS[n - 1]) for n in ss)
        rango = f"{ss[0]} a {ss[-1]}" if len(ss) > 1 else str(ss[0])
        bloques = []
        for n in ss:
            d = G.DIAPOSITIVAS[n - 1]
            parrafos = "".join(f"<p>{e(p)}</p>" for p in d["texto"])
            bloques.append(f"""
<div class="slide">
  <div class="slide-hd">
    <img src="{img_data_uri(thumbs[n - 1])}" alt="Diapositiva {n}">
    <div>
      <div class="sn">Diapositiva {n} · {fmt_min(G.minutos(G.palabras(d)))}</div>
      <div class="st">{e(d['titulo'])}</div>
      <div class="acc"><b>Qué hacer:</b> {e(d['accion'])}</div>
    </div>
  </div>
  <div class="txt">{parrafos}</div>
</div>""")
        partes.append(f"""
<section class="parte">
  <h2>{k}. {e(G.ORADORES[quien])}</h2>
  <div class="sub">{e(tema)} · diapositivas {rango} · {fmt_min(G.minutos(pal))}</div>
  {''.join(bloques)}
</section>""")

    preguntas = "".join(f"<tr><td><b>{e(q)}</b></td><td class='nw'>{e(G.ORADORES[w].split()[0])}</td><td>{e(r)}</td></tr>"
                        for q, w, r in G.PREGUNTAS)
    css = open(os.path.join(HERE, "guion.css"), encoding="utf-8").read()
    return f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<title>Guion de la presentación ejecutiva - {e(D.EMPRESA)}</title><style>{css}</style></head><body>
<header>
  <div class="kicker">PIA · {e(D.MATERIA)} · Grupo {e(D.GRUPO)}</div>
  <h1>Guion de la presentación ejecutiva</h1>
  <div class="lead">{e(D.TITULO)} — {e(D.EMPRESA)}</div>
</header>
<h3>Reparto</h3>
<table class="grid"><thead><tr><th>Orden</th><th>Integrante</th><th>Tema</th><th>Diapositivas</th><th>Tiempo aprox.</th></tr></thead>
<tbody>{reparto}</tbody></table>
<ul class="tips">
<li>Los tiempos se calcularon a {G.PALABRAS_POR_MINUTO} palabras por minuto. El total queda dentro de los 10 a 15 minutos que pide el PIA.</li>
<li>Cada parte termina con una frase para ceder la palabra al siguiente integrante.</li>
<li>El texto también está en las notas del orador del PowerPoint, con el nombre de quien habla.</li>
<li>Las instrucciones piden que todo el equipo esté presente aunque no todos expongan.</li>
</ul>
{''.join(partes)}
<section class="parte">
  <h2>Preguntas probables</h2>
  <div class="sub">Quién responde y una respuesta corta sugerida</div>
  <table class="grid"><thead><tr><th>Pregunta</th><th>Responde</th><th>Respuesta sugerida</th></tr></thead><tbody>{preguntas}</tbody></table>
</section>
</body></html>"""


def main():
    thumbs = miniaturas()
    path = os.path.join(BUILD, "guion.html")
    open(path, "w", encoding="utf-8").write(build_html(thumbs))
    tmp = os.path.join(BUILD, "guion_tmp.pdf")
    render_pdf(path, tmp)
    stamp(tmp, FINAL, title=f"Guion de la presentación ejecutiva - {D.EMPRESA}")
    print("Guion:", FINAL)


if __name__ == "__main__":
    main()
