# -*- coding: utf-8 -*-
"""Verifica que IDs, niveles, estrategias y responsables coincidan en el PDF, el
Excel y el PowerPoint, que el índice del PDF sea correcto y que estén las
correcciones de KPI/KRI."""
import os
import re
import sys

import pdfplumber
from openpyxl import load_workbook
from pptx import Presentation
from pypdf import PdfReader

import data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "entregables")
PDF = os.path.join(E, "PIA_061_Casino_Royale_Administracion_de_Riesgos_TI.pdf")
XLSX = os.path.join(E, "Matriz_de_Riesgos_Casino_Royale.xlsx")
PPTX = os.path.join(E, "Presentacion_Ejecutiva_Casino_Royale.pptx")
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip()


esperado = {r["id"]: (r["nivel"], r["estrategia"], r["responsable"]) for r in D.RIESGOS}
check(len(D.RIESGOS) == 12, "Debe haber 12 riesgos")
# regla del nivel
for r in D.RIESGOS:
    check(r["nivel"] == D.REGLA[(r["prob"], r["imp"])], f"{r['id']}: nivel no sigue la regla")
fijos = {"R1": ("Media", "Alto", "Alto"), "R2": ("Baja", "Alto", "Moderado"), "R3": ("Baja", "Alto", "Moderado"),
         "R4": ("Baja", "Medio", "Bajo"), "R5": ("Alta", "Bajo", "Moderado"), "R6": ("Media", "Alto", "Alto")}
for k, v in fijos.items():
    r = D.RIESGO[k]
    check((r["prob"], r["imp"], r["nivel"]) == v, f"{k}: no coincide con la conversión indicada")

# ---------------------------------------------------------------- Excel
wb = load_workbook(XLSX, data_only=True)
ws = wb["Matriz de riesgos"]
hdr = [c.value for c in ws[3]]
check(hdr == ["ID", "Riesgo", "Activo", "Amenaza", "Vulnerabilidad", "Fuente", "Categoría", "Probabilidad", "Impacto",
              "Nivel", "Estrategia", "Plan de respuesta", "Responsable", "Recursos", "Tiempo"], f"Encabezados Excel: {hdr}")
xl = {}
for row in ws.iter_rows(min_row=4, max_row=15, values_only=True):
    xl[row[0]] = (row[9], row[10], row[12])
check(xl == esperado, "Excel 'Matriz de riesgos' no coincide con data.py")
k = wb["KPI y KRI"]
for row in k.iter_rows(min_row=4, max_row=15, values_only=True):
    rid = row[0]
    check((row[2], row[10]) == (esperado[rid][0], esperado[rid][2]), f"Excel KPI {rid}: nivel/responsable")
    check(row[11] == D.FRECUENCIA_MONITOREO[esperado[rid][0]], f"Excel KPI {rid}: frecuencia")
check(k["G4"].value.startswith("# de inconsistencias"), "Excel: falta corrección '# de inconsistencias'")
check("cajeros" in k["D5"].value and "cajeros" in k["E5"].value, "Excel: R2 debe usar 'cajeros' en control y KPI")
m = wb["Mapa de calor"]
for ri, p in enumerate(D.PROBS):
    for ci, i in enumerate(D.IMPS):
        val = m.cell(row=4 + ri, column=3 + ci).value or ""
        ids = sorted([r["id"] for r in D.RIESGOS if r["prob"] == p and r["imp"] == i])
        check(sorted([x for x in val.split(", ") if x]) == ids, f"Excel mapa {p}/{i}: {val} != {ids}")
for name in ("Matriz de riesgos", "KPI y KRI"):
    w = wb[name]
    check(w.freeze_panes and w.auto_filter.ref, f"Excel {name}: falta encabezado fijo o filtro")

# ---------------------------------------------------------------- PowerPoint
prs = Presentation(PPTX)
check(len(prs.slides) <= 12, f"La presentación tiene {len(prs.slides)} diapositivas")
pp = {}
for n, slide in enumerate(prs.slides, start=1):
    notes = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
    check(len(notes.split()) > 60, f"Diapositiva {n}: notas del orador muy cortas o ausentes")
    for sh in slide.shapes:
        if sh.has_table:
            for row in list(sh.table.rows)[1:]:
                cells = [norm(c.text) for c in row.cells]
                pp[cells[0]] = (cells[2], cells[3], cells[5])
check(pp == esperado, f"PowerPoint: tabla de riesgos no coincide ({set(pp) ^ set(esperado)})")
palabras = sum(len((s.notes_slide.notes_text_frame.text).split()) for s in prs.slides)
print(f"Notas del orador: {palabras} palabras (~{palabras / 130:.1f} min a 130 palabras/min)")

# ---------------------------------------------------------------- PDF
reader = PdfReader(PDF)
texto = [p.extract_text() or "" for p in reader.pages]
full = norm(" ".join(texto))
pdf = {}
with pdfplumber.open(PDF) as doc:
    for page in doc.pages:
        for t in page.extract_tables():
            # tabla resumen (9 columnas); incluye su continuación en la página siguiente
            for row in t:
                if len(row) == 9 and re.fullmatch(r"R\d+", norm(row[0])) and norm(row[6]) in D.NIVELES \
                        and norm(row[7]) in ("Evitar", "Mitigar", "Transferir", "Aceptar"):
                    pdf[norm(row[0])] = (norm(row[6]), norm(row[7]), norm(row[8]))
check(pdf == esperado, f"PDF: tabla resumen no coincide: {[(k_, pdf.get(k_), v) for k_, v in esperado.items() if pdf.get(k_) != v]}")
for r in D.RIESGOS:
    check(f"{r['id']} {r['nombre']}" in full, f"PDF: falta la ficha de {r['id']}")
check("ﬁ" not in full, "PDF: hay ligaduras en el texto")
check("# de inconsistencias" in full and "# de consistencias" not in full, "PDF: corrección de inconsistencias")
check("rotación programada de cajeros" in full, "PDF: R2 KPI con 'cajeros'")
check("personal de mesa" not in full, "PDF: aún dice 'personal de mesa'")
# mapa de calor: todos los ID en la página del mapa
pag_mapa = next(i for i, t in enumerate(texto) if "5. Mapa de calor" in t and "Figura 2" in t)
for r in D.RIESGOS:
    check(re.search(rf"\b{r['id']}\b", texto[pag_mapa]), f"PDF: {r['id']} no aparece en el mapa de calor")
# índice: número impreso == página real del marcador
outline = {}
def walk(items):
    for it in items:
        if isinstance(it, list):
            walk(it)
        else:
            t = it.title.strip()
            if len(t) % 2 == 0 and t[:len(t) // 2] == t[len(t) // 2:]:
                t = t[:len(t) // 2]
            outline.setdefault(t, reader.get_destination_page_number(it) + 1)
walk(reader.outline)
toc_text = texto[1]
n_ok = 0
for title, page in outline.items():
    if title == "Índice":
        continue
    mm = re.search(re.escape(title) + r"\s*(\d+)", toc_text)
    check(mm and int(mm.group(1)) == page, f"Índice: '{title}' dice {mm.group(1) if mm else '?'} y está en {page}")
    n_ok += 1
check("Índice" in toc_text and n_ok >= 35, "Índice incompleto")
# orden de secciones
orden = ["1. Descripción de la empresa", "2. Introducción", "3. Metodología", "4. Análisis de riesgos", "5. Mapa de calor",
         "6. Monitoreo y control", "7. Comunicación", "8. Conclusión", "Referencias"]
pos = [next((i for i, t in enumerate(texto[2:], start=2) if t.lstrip().startswith(o)), None) for o in orden]
check(all(p is not None for p in pos) and pos == sorted(pos), f"Orden de secciones: {pos}")
for _n, _m in D.INTEGRANTES:
    check(_m and _n in texto[0] and _m in texto[0], f"Portada: falta {_n} o su matrícula")
check("pendiente" not in texto[0].lower(), "Portada: aún hay datos pendientes")
check(D.FECHA in texto[0] and D.DOCENTE in texto[0], "Portada: fecha o docente")

if errors:
    print("ERRORES:")
    for e_ in errors:
        print(" -", e_)
    sys.exit(1)
print(f"OK: 12 riesgos coinciden en PDF ({len(reader.pages)} págs.), Excel y PowerPoint ({len(prs.slides)} diapositivas); "
      f"índice verificado ({n_ok} entradas).")
