# -*- coding: utf-8 -*-
"""Gráficas en SVG generadas desde data.py. El mismo SVG se incrusta en el PDF y
se convierte a PNG para la presentación, así el mapa de calor se ve igual."""
from data import (RIESGOS, PROBS, IMPS, NIVELES, REGLA, COLOR, TEXTO_SOBRE,
                  FASES, FASE_TRANSVERSAL, MESES)

NAVY = "#0F1F38"
INK = "#1F2937"
MUTED = "#5B6475"
GRID = "#D7DCE3"
GOLD = "#B8901C"
FONT = "Carlito, Calibri, 'Liberation Sans', Arial, sans-serif"


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def heatmap_svg():
    cw, ch, gap = 270, 170, 6          # celda
    left, top = 150, 20                # espacio para etiquetas
    W = left + 3 * cw + 2 * gap + 20
    grid_h = 3 * ch + 2 * gap
    H = top + grid_h + 150
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT}" role="img" aria-label="Mapa de calor de riesgos: probabilidad contra impacto">']
    out.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="#FFFFFF"/>')
    # título eje Y
    cy = top + grid_h / 2
    out.append(f'<text x="34" y="{cy}" transform="rotate(-90 34 {cy})" text-anchor="middle" '
               f'font-size="20" font-weight="700" letter-spacing="3" fill="{NAVY}">PROBABILIDAD</text>')
    for ri, p in enumerate(PROBS):
        y = top + ri * (ch + gap)
        out.append(f'<text x="{left - 16}" y="{y + ch / 2 + 7}" text-anchor="end" font-size="20" '
                   f'font-weight="700" fill="{INK}">{p}</text>')
        for ci, i in enumerate(IMPS):
            x = left + ci * (cw + gap)
            lvl = REGLA[(p, i)]
            out.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="10" fill="#{COLOR[lvl]}"/>')
            out.append(f'<text x="{x + 14}" y="{y + 30}" font-size="18" font-weight="700" letter-spacing="1.5" '
                       f'fill="#{TEXTO_SOBRE[lvl]}">{lvl.upper()}</text>')
            ids = [r["id"] for r in RIESGOS if r["prob"] == p and r["imp"] == i]
            # fichas con los ID: hasta 3 por renglón
            chip_w, chip_h, cg = 76, 46, 10
            per_row = 3
            rows = [ids[k:k + per_row] for k in range(0, len(ids), per_row)]
            block_h = len(rows) * chip_h + (len(rows) - 1) * cg
            y0 = y + 44 + (ch - 44 - block_h) / 2
            for rk, row in enumerate(rows):
                row_w = len(row) * chip_w + (len(row) - 1) * cg
                x0 = x + (cw - row_w) / 2
                for k, rid in enumerate(row):
                    xx = x0 + k * (chip_w + cg)
                    yy = y0 + rk * (chip_h + cg)
                    out.append(f'<rect x="{xx}" y="{yy}" width="{chip_w}" height="{chip_h}" rx="23" fill="#FFFFFF" '
                               f'stroke="{NAVY}" stroke-opacity="0.18"/>')
                    out.append(f'<text x="{xx + chip_w / 2}" y="{yy + 31}" text-anchor="middle" font-size="24" '
                               f'font-weight="700" fill="{NAVY}">{rid}</text>')
    # etiquetas eje X
    yb = top + grid_h + 32
    for ci, i in enumerate(IMPS):
        x = left + ci * (cw + gap) + cw / 2
        out.append(f'<text x="{x}" y="{yb}" text-anchor="middle" font-size="20" font-weight="700" fill="{INK}">{i}</text>')
    out.append(f'<text x="{left + (3 * cw + 2 * gap) / 2}" y="{yb + 36}" text-anchor="middle" font-size="20" '
               f'font-weight="700" letter-spacing="3" fill="{NAVY}">IMPACTO</text>')
    # leyenda
    yl = yb + 76
    counts = {n: sum(1 for r in RIESGOS if r["nivel"] == n) for n in NIVELES}
    item_w = (3 * cw + 2 * gap) / 4
    for k, n in enumerate(NIVELES):
        x = left + k * item_w
        out.append(f'<rect x="{x}" y="{yl - 18}" width="26" height="26" rx="6" fill="#{COLOR[n]}"/>')
        out.append(f'<text x="{x + 36}" y="{yl + 3}" font-size="20" fill="{INK}"><tspan font-weight="700">{n}</tspan>'
                   f' ({counts[n]})</text>')
    out.append("</svg>")
    return "\n".join(out)


def gantt_svg():
    label_w, wk, row_h, top = 330, 30, 48, 66
    weeks = 24
    rows = FASES + [dict(n="", **FASE_TRANSVERSAL)]
    W = label_w + weeks * wk + 20
    H = top + len(rows) * row_h + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
           f'font-family="{FONT}" role="img" aria-label="Línea del tiempo de la implementación de ISO 31000">']
    out.append(f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>')
    # meses (4 semanas cada uno)
    for m, name in enumerate(MESES):
        x = label_w + m * 4 * wk
        fill = "#F1F3F6" if m % 2 == 0 else "#FFFFFF"
        out.append(f'<rect x="{x}" y="{top - 6}" width="{4 * wk}" height="{len(rows) * row_h + 6}" fill="{fill}"/>')
        out.append(f'<text x="{x + 2 * wk}" y="24" text-anchor="middle" font-size="20" font-weight="700" fill="{NAVY}">{name} 2026</text>')
        for s in range(4):
            out.append(f'<text x="{x + s * wk + wk / 2}" y="48" text-anchor="middle" font-size="14" fill="{MUTED}">{m * 4 + s + 1}</text>')
    out.append(f'<text x="8" y="50" font-size="14" fill="{MUTED}">Semana →</text>')
    for k, f in enumerate(rows):
        y = top + k * row_h
        trans = f["n"] == ""
        label = f["nombre"] if trans else f'{f["n"]}. {f["nombre"]}'
        if trans:
            label = "Comunicación y consulta"
        out.append(f'<text x="8" y="{y + row_h / 2 + 5}" font-size="19" font-weight="{700 if not trans else 400}" '
                   f'fill="{INK}">{_esc(label)}</text>')
        x = label_w + (f["ini"] - 1) * wk + 2
        w = (f["fin"] - f["ini"] + 1) * wk - 4
        color = GOLD if trans else NAVY
        out.append(f'<rect x="{x}" y="{y + 9}" width="{w}" height="{row_h - 18}" rx="6" fill="{color}"/>')
        txt = f'Sem {f["ini"]}–{f["fin"]}'
        out.append(f'<text x="{x + w / 2}" y="{y + row_h / 2 + 5}" text-anchor="middle" font-size="15" '
                   f'font-weight="700" fill="#FFFFFF">{txt}</text>')
    # hito final
    xh = label_w + weeks * wk
    yh = top + len(rows) * row_h + 22
    out.append(f'<text x="{xh}" y="{yh}" text-anchor="end" font-size="15" fill="{MUTED}">'
               f'Fin de la implementación: semana 24 (octubre 2026) · Primera revisión anual: noviembre 2027</text>')
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    import os
    os.makedirs("../build", exist_ok=True)
    open("../build/mapa_calor.svg", "w").write(heatmap_svg())
    open("../build/linea_tiempo.svg", "w").write(gantt_svg())
