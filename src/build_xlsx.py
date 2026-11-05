# -*- coding: utf-8 -*-
"""Genera la matriz de riesgos en Excel a partir de data.py."""
import math
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.worksheet.pagebreak import Break

import data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "entregables", "Matriz_de_Riesgos_Casino_Royale.xlsx")

FONT = "Arial"
NAVY = "0F1F38"
SOFT = "F3F5F8"
thin = Side(style="thin", color="C9CFD8")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(wrap_text=True, vertical="center", horizontal="center")

MAT = "Matriz de riesgos"
KPI = "KPI y KRI"
MAPA = "Mapa de calor"
FIRST, LAST = 4, 3 + len(D.RIESGOS)  # filas de datos en la matriz


def fill(hex_):
    return PatternFill("solid", start_color=hex_, end_color=hex_)


def title(ws, text, sub, ncols):
    ws["A1"] = text
    ws["A1"].font = Font(name=FONT, size=14, bold=True, color=NAVY)
    ws["A2"] = sub
    ws["A2"].font = Font(name=FONT, size=9, italic=True, color="5B6475")
    ws.row_dimensions[1].height = 22


def header(ws, row, names, widths):
    for c, (n, w) in enumerate(zip(names, widths), start=1):
        cell = ws.cell(row=row, column=c, value=n)
        cell.font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        cell.fill = fill(NAVY)
        cell.alignment = CENTER
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(c)].width = w
    ws.row_dimensions[row].height = 30


def est_height(values, widths, base=11.6):
    lines = 1
    for v, w in zip(values, widths):
        if v is None:
            continue
        txt = str(v)
        if txt.startswith("="):
            continue
        n = sum(max(1, math.ceil(len(part) / max(w * 1.18, 1))) for part in txt.split("\n"))
        lines = max(lines, n)
    return max(18, lines * base + 6)


def level_cf(ws, rng, first_cell):
    for n in D.NIVELES:
        ws.conditional_formatting.add(rng, FormulaRule(
            formula=[f'{first_cell}="{n}"'], stopIfTrue=True,
            fill=fill(D.COLOR[n]), font=Font(name=FONT, bold=True, color=D.TEXTO_SOBRE[n])))


def print_setup(ws, title_rows, title_cols=None, fit_width=1):
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = ws.PAPERSIZE_LETTER
    ws.page_margins.left = ws.page_margins.right = 0.4
    ws.page_margins.top = 0.55
    ws.page_margins.bottom = 0.6
    ws.print_title_rows = title_rows
    if title_cols:
        ws.print_title_cols = title_cols
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = fit_width
    ws.page_setup.fitToHeight = 0
    ws.print_options.horizontalCentered = True
    ws.oddHeader.left.text = f"{D.EMPRESA} — PIA {D.MATERIA} (Grupo {D.GRUPO})"
    ws.oddHeader.left.size = 8
    ws.oddFooter.center.text = "Página &P de &N"
    ws.oddFooter.center.size = 8
    ws.oddFooter.right.text = "&A"
    ws.oddFooter.right.size = 8


def nivel_formula(r):
    h, i = f"H{r}", f"I{r}"
    return (f'=IF(OR({h}="",{i}=""),"",'
            f'IF(AND({h}="Alta",{i}="Alto"),"Crítico",'
            f'IF(OR(AND({h}="Alta",{i}="Medio"),AND({h}="Media",{i}="Alto")),"Alto",'
            f'IF(OR(AND({h}="Alta",{i}="Bajo"),AND({h}="Media",{i}="Medio"),AND({h}="Baja",{i}="Alto")),"Moderado",'
            f'"Bajo"))))')


def hoja_matriz(wb):
    ws = wb.active
    ws.title = MAT
    cols = ["ID", "Riesgo", "Activo", "Amenaza", "Vulnerabilidad", "Fuente", "Categoría", "Probabilidad",
            "Impacto", "Nivel", "Estrategia", "Plan de respuesta", "Responsable", "Recursos", "Tiempo"]
    widths = [6, 24, 24, 26, 26, 10, 13, 12.5, 10, 11, 12, 52, 20, 28, 22]
    title(ws, f"Matriz de riesgos — {D.EMPRESA}",
          "Caso académico ficticio. El nivel se calcula con fórmula a partir de Probabilidad e Impacto (regla en la hoja «Mapa de calor»). "
          "Celdas editables: Probabilidad, Impacto, Estrategia, Fuente y Categoría (listas desplegables).", len(cols))
    header(ws, 3, cols, widths)
    for k, r in enumerate(D.RIESGOS):
        row = FIRST + k
        plan = "\n".join(f"{n}. {a}" for n, a in enumerate(r["acciones"], start=1))
        vals = [r["id"], r["nombre"], r["activo"], r["amenaza"], r["vulnerabilidad"], r["fuente"], r["categoria"],
                r["prob"], r["imp"], nivel_formula(row), r["estrategia"], plan, r["responsable"], r["recursos"], r["tiempo"]]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=9, bold=(c in (1, 2)), color=NAVY if c in (1, 2) else "1F2937")
            cell.alignment = CENTER if c in (1, 6, 7, 8, 9, 10, 11) else WRAP
            cell.border = BORDER
            if k % 2 == 1 and c != 10:
                cell.fill = fill("FAFBFC")
        ws.row_dimensions[row].height = est_height(vals, widths)
    level_cf(ws, f"J{FIRST}:J{LAST}", f"J{FIRST}")
    ws.freeze_panes = f"C{FIRST}"
    ws.auto_filter.ref = f"A3:O{LAST}"
    # listas desplegables
    for rng, opts in [(f"F{FIRST}:F{LAST}", "Externa,Interna"),
                      (f"G{FIRST}:G{LAST}", "Financiero,Operativo,Tecnológico,Legal,Reputacional"),
                      (f"H{FIRST}:H{LAST}", "Alta,Media,Baja"),
                      (f"I{FIRST}:I{LAST}", "Alto,Medio,Bajo"),
                      (f"K{FIRST}:K{LAST}", "Evitar,Mitigar,Transferir,Aceptar")]:
        dv = DataValidation(type="list", formula1=f'"{opts}"', allow_blank=False, showErrorMessage=True,
                            errorTitle="Valor no válido", error="Elige un valor de la lista.")
        dv.add(rng)
        ws.add_data_validation(dv)
    # resumen al pie
    srow = LAST + 2
    ws.cell(row=srow, column=2, value="Riesgos por nivel").font = Font(name=FONT, size=10, bold=True, color=NAVY)
    for k, n in enumerate(D.NIVELES):
        a = ws.cell(row=srow + 1 + k, column=2, value=n)
        a.font = Font(name=FONT, size=9, bold=True, color=D.TEXTO_SOBRE[n])
        a.fill = fill(D.COLOR[n])
        a.border = BORDER
        b = ws.cell(row=srow + 1 + k, column=3, value=f'=COUNTIF($J${FIRST}:$J${LAST},B{srow + 1 + k})')
        b.font = Font(name=FONT, size=9)
        b.alignment = Alignment(horizontal="center")
        b.border = BORDER
    t = ws.cell(row=srow + 5, column=2, value="Total")
    t.font = Font(name=FONT, size=9, bold=True)
    ws.cell(row=srow + 5, column=3, value=f"=SUM(C{srow + 1}:C{srow + 4})").alignment = Alignment(horizontal="center")
    print_setup(ws, "3:3", "A:B", fit_width=2)
    ws.col_breaks.append(Break(id=10))  # página 1: ID a Nivel; página 2: Estrategia a Tiempo
    ws.print_area = f"A1:O{srow + 5}"
    return ws


def hoja_kpi(wb):
    ws = wb.create_sheet(KPI)
    cols = ["ID", "Riesgo", "Nivel", "Control", "KPI (desempeño del control)", "Meta KPI", "KRI (nivel del riesgo)",
            "Umbral KRI", "Interpretación", "Acción", "Responsable", "Frecuencia de monitoreo", "Origen"]
    widths = [6, 24, 11, 28, 30, 10, 30, 13, 34, 32, 20, 13, 20]
    title(ws, f"KPI y KRI por riesgo — {D.EMPRESA}",
          "R1, R2 y R5 se retoman de la actividad del 18/10/2026 (corregido: «# de inconsistencias» y «cajeros» en control y KPI). "
          "Riesgo, Nivel y Responsable se leen de la hoja «Matriz de riesgos».", len(cols))
    header(ws, 3, cols, widths)
    look = lambda col, r: (f"=INDEX('{MAT}'!${col}${FIRST}:${col}${LAST},MATCH($A{r},'{MAT}'!$A${FIRST}:$A${LAST},0))")
    for k, r in enumerate(D.RIESGOS):
        row = 4 + k
        q = D.KPI_KRI[r["id"]]
        freq = (f'=IF(C{row}="Crítico","Semanal",IF(C{row}="Alto","Quincenal",'
                f'IF(C{row}="Moderado","Mensual",IF(C{row}="Bajo","Trimestral",""))))')
        vals = [r["id"], look("B", row), look("J", row), q["control"], q["kpi"], q["meta"], q["kri"], q["umbral"],
                q["interpretacion"], q["accion"], look("M", row), freq, q["origen"]]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=row, column=c, value=v)
            cell.font = Font(name=FONT, size=9, bold=(c in (1, 2)), color=NAVY if c in (1, 2) else "1F2937")
            cell.alignment = CENTER if c in (1, 3, 6, 8, 12) else WRAP
            cell.border = BORDER
            if k % 2 == 1 and c != 3:
                cell.fill = fill("FAFBFC")
        shown = [r["id"], r["nombre"], r["nivel"]] + vals[3:10] + [r["responsable"], r["frecuencia"], q["origen"]]
        ws.row_dimensions[row].height = est_height(shown, widths)
    last = 3 + len(D.RIESGOS)
    level_cf(ws, f"C4:C{last}", "C4")
    ws.freeze_panes = "C4"
    ws.auto_filter.ref = f"A3:M{last}"
    print_setup(ws, "3:3", "A:B", fit_width=2)
    ws.col_breaks.append(Break(id=8))  # página 1: ID a Umbral KRI; página 2: Interpretación a Origen
    return ws


def hoja_mapa(wb):
    ws = wb.create_sheet(MAPA)
    title(ws, f"Mapa de calor — {D.EMPRESA}",
          "Probabilidad contra impacto. Los ID de cada celda se calculan con fórmula a partir de la hoja «Matriz de riesgos».", 6)
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 16
    for col in "CDE":
        ws.column_dimensions[col].width = 26
    ws.column_dimensions["F"].width = 3
    ws.column_dimensions["G"].width = 16
    ws.column_dimensions["H"].width = 62
    # eje Y
    ws.merge_cells("A4:A6")
    a = ws["A4"]
    a.value = "PROBABILIDAD"
    a.font = Font(name=FONT, size=10, bold=True, color=NAVY)
    a.alignment = Alignment(text_rotation=90, horizontal="center", vertical="center")
    mat = f"'{MAT}'"
    for ri, p in enumerate(D.PROBS):
        row = 4 + ri
        ws.row_dimensions[row].height = 78
        lab = ws.cell(row=row, column=2, value=p)
        lab.font = Font(name=FONT, size=11, bold=True, color=NAVY)
        lab.alignment = Alignment(horizontal="right", vertical="center", indent=1)
        for ci, i in enumerate(D.IMPS):
            col = 3 + ci
            lvl = D.REGLA[(p, i)]
            ref = f"{get_column_letter(col)}{row}"
            f = (f'=_xlfn.TEXTJOIN(", ",TRUE,IF(({mat}!$H${FIRST}:$H${LAST}="{p}")*({mat}!$I${FIRST}:$I${LAST}="{i}"),'
                 f'{mat}!$A${FIRST}:$A${LAST},""))')
            cell = ws.cell(row=row, column=col)
            cell.value = ArrayFormula(ref, f)
            cell.fill = fill(D.COLOR[lvl])
            cell.font = Font(name=FONT, size=13, bold=True, color=D.TEXTO_SOBRE[lvl])
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = Border(left=Side(style="medium", color="FFFFFF"), right=Side(style="medium", color="FFFFFF"),
                                 top=Side(style="medium", color="FFFFFF"), bottom=Side(style="medium", color="FFFFFF"))
    for ci, i in enumerate(D.IMPS):
        c = ws.cell(row=7, column=3 + ci, value=i)
        c.font = Font(name=FONT, size=11, bold=True, color=NAVY)
        c.alignment = Alignment(horizontal="center")
    ws.merge_cells("C8:E8")
    x = ws["C8"]
    x.value = "IMPACTO"
    x.font = Font(name=FONT, size=10, bold=True, color=NAVY)
    x.alignment = Alignment(horizontal="center")
    # nivel de cada celda (texto pequeño debajo)
    ws["B10"] = "Nivel de cada celda"
    ws["B10"].font = Font(name=FONT, size=10, bold=True, color=NAVY)
    for ri, p in enumerate(D.PROBS):
        row = 11 + ri
        ws.cell(row=row, column=2, value=p).font = Font(name=FONT, size=9, bold=True)
        for ci, i in enumerate(D.IMPS):
            lvl = D.REGLA[(p, i)]
            c = ws.cell(row=row, column=3 + ci, value=lvl)
            c.fill = fill(D.COLOR[lvl])
            c.font = Font(name=FONT, size=9, bold=True, color=D.TEXTO_SOBRE[lvl])
            c.alignment = Alignment(horizontal="center")
            c.border = BORDER
    for ci, i in enumerate(D.IMPS):
        c = ws.cell(row=14, column=3 + ci, value=f"Impacto {i}")
        c.font = Font(name=FONT, size=9, italic=True)
        c.alignment = Alignment(horizontal="center")
    # leyenda: regla, conteo y frecuencia
    reglas = {
        "Crítico": "Alta + Alto",
        "Alto": "Alta + Medio, o Media + Alto",
        "Moderado": "Alta + Bajo, Media + Medio, o Baja + Alto",
        "Bajo": "Media + Bajo, Baja + Medio, o Baja + Bajo",
    }
    ws["G10"] = "Nivel"
    ws["H10"] = "Regla (probabilidad + impacto) · riesgos · frecuencia de monitoreo"
    for c in ("G10", "H10"):
        ws[c].font = Font(name=FONT, size=10, bold=True, color="FFFFFF")
        ws[c].fill = fill(NAVY)
    for k, n in enumerate(D.NIVELES):
        row = 11 + k
        g = ws.cell(row=row, column=7, value=n)
        g.fill = fill(D.COLOR[n])
        g.font = Font(name=FONT, size=9, bold=True, color=D.TEXTO_SOBRE[n])
        g.alignment = Alignment(horizontal="center")
        g.border = BORDER
        h_ = ws.cell(row=row, column=8,
                     value=f'="{reglas[n]} · "&COUNTIF({mat}!$J${FIRST}:$J${LAST},G{row})&" riesgo(s) · {D.FRECUENCIA_MONITOREO[n]}"')
        h_.font = Font(name=FONT, size=9)
        h_.border = BORDER
    print_setup(ws, None, None, fit_width=1)
    ws.page_setup.fitToHeight = 1
    ws.print_area = "A1:H15"
    ws.sheet_view.showGridLines = False
    return ws


def main():
    wb = Workbook()
    hoja_matriz(wb)
    hoja_kpi(wb)
    hoja_mapa(wb)
    for ws in wb.worksheets:
        ws.sheet_view.zoomScale = 90
    wb.properties.title = f"Matriz de riesgos - {D.EMPRESA}"
    wb.properties.creator = ", ".join(n for n, _ in D.INTEGRANTES)
    wb.save(OUT)
    print("XLSX:", OUT)


if __name__ == "__main__":
    main()
