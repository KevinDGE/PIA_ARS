# -*- coding: utf-8 -*-
"""Exporta data.py a JSON y genera los PNG (mapa de calor e íconos) para la presentación."""
import json, os, subprocess
import data as D
from charts import heatmap_svg, gantt_svg

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(os.path.dirname(HERE), "build")
os.makedirs(BUILD, exist_ok=True)
keys = ["EMPRESA", "MATERIA", "GRUPO", "UNIVERSIDAD", "FACULTAD", "DOCENTE", "FECHA", "TITULO", "INTEGRANTES",
        "RIESGOS", "KPI_KRI", "COLOR", "TEXTO_SOBRE", "TINTE", "NIVELES", "FASES", "FASE_TRANSVERSAL", "RETOS",
        "FRECUENCIA_MONITOREO", "DURACION", "MESES"]
json.dump({k: getattr(D, k) for k in keys}, open(os.path.join(BUILD, "data.json"), "w"), ensure_ascii=False, indent=1)
for name, svg in [("mapa_calor", heatmap_svg()), ("linea_tiempo", gantt_svg())]:
    p = os.path.join(BUILD, name + ".svg")
    open(p, "w").write(svg)
    subprocess.run(["node", os.path.join(HERE, "render.js"), "png", p, os.path.join(BUILD, name + ".png"), "3"], check=True)
# íconos: glifos monocromos de DejaVu Sans en blanco
ICONOS = {"dinero": "$", "ley": "⚖", "confianza": "★", "engrane": "⚙", "check": "✓",
          "alerta": "!", "personas": "☺", "reloj": "⌚"}
for k, g in ICONOS.items():
    p = os.path.join(BUILD, f"ico_{k}.svg")
    open(p, "w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128" width="128" height="128">'
                       f'<text x="64" y="64" dominant-baseline="central" text-anchor="middle" font-family="DejaVu Sans" '
                       f'font-weight="bold" font-size="84" fill="#FFFFFF">{g}</text></svg>')
    subprocess.run(["node", os.path.join(HERE, "render.js"), "pngt", p, os.path.join(BUILD, f"ico_{k}.png"), "3"], check=True)
print("ok")
