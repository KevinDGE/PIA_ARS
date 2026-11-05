# -*- coding: utf-8 -*-
"""Genera el documento del PIA en HTML y lo convierte a PDF con Chromium.
Dos pasadas: la primera calcula en qué página cae cada sección (a partir de los
marcadores del PDF) y la segunda escribe esos números en el índice."""
import base64
import html
import io
import json
import os
import subprocess
import sys

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import data as D
from charts import heatmap_svg, gantt_svg

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BUILD = os.path.join(ROOT, "build")
OUT = os.path.join(ROOT, "entregables")
LOGOS = os.path.join(ROOT, "assets", "logos")
os.makedirs(BUILD, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

e = html.escape


def img_data_uri(path):
    ext = os.path.splitext(path)[1].lower().strip(".")
    mime = "image/png" if ext == "png" else "image/jpeg" if ext in ("jpg", "jpeg") else "image/svg+xml"
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()


def find_logo(stem):
    for ext in ("png", "jpg", "jpeg", "svg"):
        p = os.path.join(LOGOS, f"{stem}.{ext}")
        if os.path.exists(p):
            return p
    return None


def badge(nivel):
    return f'<span class="badge" style="background:#{D.COLOR[nivel]};color:#{D.TEXTO_SOBRE[nivel]}">{e(nivel)}</span>'


def ul(items):
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


# ------------------------------------------------------------------ índice
# (nivel, id, texto)  -> el texto debe coincidir con el encabezado
TOC = []


def h(level, hid, text):
    TOC.append((level, hid, text))
    tag = "h1" if level == 1 else "h2"
    return f'<{tag} id="{hid}">{e(text)}</{tag}>'


# ------------------------------------------------------------------ secciones
def portada():
    def logo_box(stem, etiqueta):
        p = find_logo(stem)
        if p:
            return f'<div class="logo-box"><img src="{img_data_uri(p)}" alt="{e(etiqueta)}"></div>'
        return (f'<div class="logo-box pend"><span>{e(etiqueta)}</span>'
                f'<small>PENDIENTE: agregar archivo assets/logos/{stem}.png</small></div>')

    casino = img_data_uri(os.path.join(LOGOS, "casino_royale_blanco.png"))
    filas = "".join(
        f'<tr><td>{e(n)}</td><td class="{"" if m else "pend-txt"}">{e(m) if m else "Matrícula pendiente"}</td></tr>'
        for n, m in D.INTEGRANTES)
    facultad = e(D.FACULTAD) if D.FACULTAD else '<span class="pend-txt">Facultad: pendiente</span>'
    return f"""
<section class="cover">
  <div class="cover-logos">
    {logo_box("uanl", "Logo UANL")}
    {logo_box("facultad", "Logo de la facultad")}
  </div>
  <div class="cover-uni">{e(D.UNIVERSIDAD)}<br>{facultad}</div>
  <div class="cover-panel">
    <img class="casino-logo" src="{casino}" alt="Logo de Casino Royale Enterprises">
    <div class="cover-kicker">Producto Integrador de Aprendizaje (PIA)</div>
    <div class="cover-title">{e(D.TITULO)}</div>
    <div class="cover-sub">Caso académico: {e(D.EMPRESA)}</div>
  </div>
  <table class="cover-data">
    <tr><th>Materia</th><td>{e(D.MATERIA)}</td></tr>
    <tr><th>Grupo</th><td>{e(D.GRUPO)}</td></tr>
    <tr><th>Docente</th><td>{e(D.DOCENTE)}</td></tr>
    <tr><th>Fecha</th><td>{e(D.FECHA)}</td></tr>
  </table>
  <table class="cover-team">
    <thead><tr><th>Integrantes del equipo</th><th>Matrícula</th></tr></thead>
    <tbody>{filas}</tbody>
  </table>
  <p class="cover-note">Casino Royale Enterprises es una empresa ficticia creada para este trabajo académico. Su misión, visión, sistemas y datos son supuestos del caso.</p>
</section>"""


def indice(pages):
    rows = []
    for level, hid, text in TOC:
        pg = pages.get(hid, "00")
        rows.append(f'<li class="toc-l{level}"><a href="#{hid}"><span class="t">{e(text)}</span>'
                    f'<span class="dots"></span><span class="p">{pg}</span></a></li>')
    return f"""
<section class="toc page">
  <h1 class="toc-title">Índice</h1>
  <ol class="toc-list">{''.join(rows)}</ol>
</section>"""


def sec_empresa():
    I = D.EMPRESA_INFO
    tec = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in I["tecnologias"])
    valores = "".join(f'<div class="val"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in I["valores"])
    return f"""
<section class="page">
{h(1, "s1", "1. Descripción de la empresa y del área de TI")}
<p class="note">Caso académico ficticio. Los datos de esta sección son supuestos elaborados por el equipo para desarrollar el plan; no describen a una empresa real.</p>
{h(2, "s1-1", "1.1 Datos generales")}
<table class="kv">
  <tr><th>Nombre</th><td>{e(D.EMPRESA)}</td></tr>
  <tr><th>Giro</th><td>{e(I["giro"])}</td></tr>
  <tr><th>Clientes y mercado objetivo</th><td>{e(I["clientes"])}</td></tr>
  <tr><th>Ubicación y cobertura</th><td>{e(I["ubicacion"])}</td></tr>
</table>
{h(2, "s1-2", "1.2 Misión y visión de la empresa")}
<div class="two">
  <div class="card"><div class="lbl">Misión</div><p>{e(I["mision"])}</p></div>
  <div class="card"><div class="lbl">Visión</div><p>{e(I["vision"])}</p></div>
</div>
{h(2, "s1-3", "1.3 Misión y visión del área de TI")}
<div class="two">
  <div class="card"><div class="lbl">Misión de TI</div><p>{e(I["mision_ti"])}</p></div>
  <div class="card"><div class="lbl">Visión de TI</div><p>{e(I["vision_ti"])}</p></div>
</div>
{h(2, "s1-4", "1.4 Productos y servicios")}
{ul(I["productos"])}
{h(2, "s1-5", "1.5 Valores")}
<div class="vals">{valores}</div>
{h(2, "s1-6", "1.6 Área de TI: estructura, sistemas y tecnologías")}
<p>El área de TI depende de la Dirección General y está integrada por: {e(", ".join(I["estructura_ti"]))}. El área de Vigilancia (CCTV) depende de Seguridad, pero usa la infraestructura que administra TI.</p>
<table class="kv">{tec}</table>
</section>"""


def sec_intro():
    roles = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in D.ROLES)
    kpi = "".join(f"<tr><td>{e(a)}</td><td class='c'>{e(b)}</td></tr>" for a, b in D.KPI_PROGRAMA)
    kri = "".join(f"<tr><td>{e(a)}</td><td class='c'>{e(b)}</td></tr>" for a, b in D.KRI_PROGRAMA)
    return f"""
<section class="page">
{h(1, "s2", "2. Introducción")}
{h(2, "s2-1", "2.1 Objetivo del plan")}
<p>Identificar, analizar, valorar y tratar los riesgos de TI de {e(D.EMPRESA)} y los riesgos operativos que dependen de la tecnología, para proteger los ingresos del juego, la información de los clientes, el cumplimiento legal y la continuidad de la operación. El plan define quién es responsable de cada riesgo, qué se hará, con qué recursos y en qué plazo, y cómo se medirá el avance.</p>
{h(2, "s2-2", "2.2 Alcance")}
<p>El plan cubre al área de TI y a los procesos de negocio de la sala principal que dependen de ella:</p>
<ul>
<li>Juego en mesas y en máquinas tragamonedas.</li>
<li>Caja, pagos con tarjeta y pago de premios.</li>
<li>Videovigilancia (CCTV).</li>
<li>Programa de lealtad y datos de clientes.</li>
<li>Cumplimiento en prevención de lavado de dinero (PLD), conforme a la Ley Federal para la Prevención e Identificación de Operaciones con Recursos de Procedencia Ilícita, LFPIORPI (Cámara de Diputados del H. Congreso de la Unión, 2025b), y en protección de datos personales, conforme a la Ley Federal de Protección de Datos Personales en Posesión de los Particulares, LFPDPPP (Cámara de Diputados del H. Congreso de la Unión, 2025a).</li>
</ul>
<p>Quedan fuera los riesgos de construcción, protección civil y los del restaurante-bar que no involucran sistemas. El plan aplica de noviembre de 2026 a octubre de 2027 y se renueva cada año.</p>
{h(2, "s2-3", "2.3 Responsables de la gestión de riesgos")}
<table class="kv">{roles}</table>
{h(2, "s2-4", "2.4 KPI y KRI")}
<p>Un <b>KPI</b> (indicador clave de desempeño) mide qué tan bien funciona un control. Un <b>KRI</b> (indicador clave de riesgo) mide qué tan expuesta está la empresa. Leídos juntos permiten saber si un control realmente reduce el riesgo y actuar antes de que el problema crezca. Cada uno de los 12 riesgos tiene su control, KPI, KRI, interpretación y acción en el tablero de la sección 6.4. Además, el plan completo se mide con estos indicadores:</p>
<div class="two">
<table class="grid"><thead><tr><th>KPI del programa</th><th>Meta</th></tr></thead><tbody>{kpi}</tbody></table>
<table class="grid"><thead><tr><th>KRI del programa</th><th>Meta</th></tr></thead><tbody>{kri}</tbody></table>
</div>
</section>"""


def sec_metodologia():
    cats = "".join(f"<tr><th>{e(c)}</th><td>{e(d)}</td><td class='c'>{e(', '.join(ids))}</td></tr>" for c, d, ids in D.CATEGORIAS)
    foda = "".join(f'<div class="foda f{k}"><div class="lbl">{e(t)}</div>{ul(items)}</div>'
                   for k, (t, items) in enumerate(D.FODA.items()))
    ep = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in D.ESCALA_PROB)
    ei = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in D.ESCALA_IMP)
    # matriz de la regla
    regla = "<tr><th class='corner'>Probabilidad \\ Impacto</th>" + "".join(f"<th>{i}</th>" for i in D.IMPS) + "</tr>"
    for p in D.PROBS:
        regla += f"<tr><th>{p}</th>" + "".join(
            f"<td class='c' style='background:#{D.COLOR[D.REGLA[(p, i)]]};color:#{D.TEXTO_SOBRE[D.REGLA[(p, i)]]};font-weight:700'>{D.REGLA[(p, i)]}</td>"
            for i in D.IMPS) + "</tr>"
    conv = "".join(f"<tr><td>{e(a)}</td><td class='c'>{e(b)}</td></tr>" for a, b in D.CONVERSION_PROB)
    convi = "".join(f"<tr><td>{e(a)}</td><td class='c'>{e(b)}</td></tr>" for a, b in D.CONVERSION_IMP)
    fases = "".join(
        f"<tr><td class='c'><b>{f['n']}</b></td><td><b>{e(f['nombre'])}</b><br><span class='muted'>ISO 31000: {e(f['clausula'])}</span></td>"
        f"<td>{e(f['que'])}</td><td>{e(f['quien'])}</td><td class='c nw'>Sem {f['ini']}–{f['fin']}</td></tr>" for f in D.FASES)
    T = D.FASE_TRANSVERSAL
    fases += (f"<tr><td class='c'>—</td><td><b>Comunicación y consulta</b><br><span class='muted'>ISO 31000: {e(T['clausula'])}</span></td>"
              f"<td>Se informa y consulta a cada área durante todas las fases.</td><td>{e(T['quien'])}</td><td class='c nw'>Sem 1–24</td></tr>")
    retos = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in D.RETOS)
    return f"""
<section class="page">
{h(1, "s3", "3. Metodología")}
{h(2, "s3-1", "3.1 Estándar: ISO 31000:2018")}
<p>El estándar principal es <b>ISO 31000:2018, Gestión del riesgo — Directrices</b> (International Organization for Standardization [ISO], 2018). Se eligió porque sirve para cualquier tipo de organización y de riesgo, por lo que permite tratar en una sola matriz los riesgos tecnológicos y los de la operación de juego, la caja y el cumplimiento legal. ISO 31000 es una guía y no se certifica: su valor está en dar un lenguaje y un método comunes.</p>
<p>El estándar tiene tres partes que se aplicaron en el casino:</p>
<div class="three">
  <div class="card"><div class="lbl">Principios</div><p>La gestión del riesgo debe ser integrada, estructurada y exhaustiva, adaptada, inclusiva y dinámica; usar la mejor información disponible; considerar factores humanos y culturales, y mejorar continuamente.</p></div>
  <div class="card"><div class="lbl">Marco de referencia</div><p>Liderazgo y compromiso de la dirección, integración, diseño, implementación, valoración y mejora del sistema de gestión de riesgos.</p></div>
  <div class="card"><div class="lbl">Proceso</div><p>Comunicación y consulta; alcance, contexto y criterios; evaluación del riesgo (identificar, analizar y valorar); tratamiento; seguimiento y revisión; registro e informe.</p></div>
</div>
<p>Para escoger las técnicas de identificación y análisis se tomó como apoyo la norma IEC 31010:2019, que describe técnicas como la lluvia de ideas, las entrevistas y las encuestas (International Electrotechnical Commission [IEC], 2019).</p>
{h(2, "s3-2", "3.2 Herramientas de identificación y análisis")}
<table class="kv">
<tr><th>Encuestas</th><td>Cuestionario anónimo de 10 preguntas al personal de caja, mesas, vigilancia, TI y administración sobre fallas, malas prácticas y situaciones de riesgo que han visto. Ayudó a detectar R5, R12 y el uso de cuentas compartidas (R9).</td></tr>
<tr><th>Entrevistas</th><td>Entrevistas de 45 minutos con los responsables de TI, seguridad de la información, caja, operaciones de juego, vigilancia y cumplimiento PLD para conocer controles actuales, incidentes previos y dependencias entre sistemas.</td></tr>
<tr><th>Lluvia de ideas</th><td>Dos talleres con el Comité de Riesgos para proponer riesgos sin juzgarlos, agruparlos por categoría y acordar su probabilidad e impacto. De ahí surgieron R7, R8, R10 y R11.</td></tr>
<tr><th>Análisis FODA</th><td>Revisión de fortalezas y debilidades internas del área de TI y de oportunidades y amenazas externas, para relacionar cada debilidad con una amenaza y obtener riesgos concretos.</td></tr>
</table>
<div class="foda-grid">{foda}</div>
{h(2, "s3-3", "3.3 Clasificación de riesgos")}
<table class="grid"><thead><tr><th>Categoría</th><th>Qué incluye</th><th>Riesgos</th></tr></thead><tbody>{cats}</tbody></table>
{h(2, "s3-4", "3.4 Criterios de valoración")}
<div class="two">
<table class="kv small"><tr><th colspan="2" class="hd">Probabilidad</th></tr>{ep}</table>
<table class="kv small"><tr><th colspan="2" class="hd">Impacto</th></tr>{ei}</table>
</div>
<p>El nivel de riesgo se obtiene combinando probabilidad e impacto con la siguiente regla:</p>
<table class="grid regla">{regla}</table>
<p>Los seis riesgos de la matriz anterior (10 de octubre de 2026) estaban en una escala de 5x5. Para el PIA se convirtieron a la escala 3x3 así:</p>
<div class="two">
<table class="grid small"><thead><tr><th>Probabilidad 5x5</th><th>Escala PIA</th></tr></thead><tbody>{conv}</tbody></table>
<table class="grid small"><thead><tr><th>Impacto 5x5</th><th>Escala PIA</th></tr></thead><tbody>{convi}</tbody></table>
</div>
<p>Con la conversión, R2 pasó de Medio a Moderado, R3 de Alto a Moderado y R5 de Medio a Moderado. R1 y R6 se mantienen en Alto y R4 en Bajo.</p>
{h(2, "s3-5", "3.5 Implementación de ISO 31000 en el casino (caso simulado)")}
<p><b>Qué se busca con el estándar.</b> Que todas las áreas usen los mismos criterios para medir riesgos, que las inversiones en seguridad se decidan por prioridad y no por urgencia, y que los riesgos se revisen como parte de las decisiones del negocio y no solo cuando ocurre un incidente.</p>
<p><b>Quién está a cargo.</b> La Dirección General patrocina el proyecto y el Gerente de Riesgos y Cumplimiento lo lidera, con el apoyo del Director de TI y del Comité de Riesgos.</p>
<p><b>Duración.</b> La implementación se llevó en seis fases durante {e(D.DURACION)}, más una actividad de comunicación y consulta que acompañó todo el proyecto.</p>
<table class="grid small"><thead><tr><th>#</th><th>Fase</th><th>Qué se hizo</th><th>Responsable</th><th>Tiempo</th></tr></thead><tbody>{fases}</tbody></table>
<figure class="fig">{gantt_svg()}<figcaption>Figura 1. Línea del tiempo de la implementación de ISO 31000 (caso simulado).</figcaption></figure>
<p><b>Problemas y retos que se enfrentaron.</b></p>
<table class="grid small"><thead><tr><th>Reto</th><th>Qué pasó</th><th>Cómo se resolvió</th></tr></thead><tbody>{retos}</tbody></table>
<p><b>Cada cuándo se renueva.</b></p>
<ul>
<li>Matriz de riesgos y mapa de calor: cada trimestre.</li>
<li>KPI y KRI: según el nivel del riesgo (sección 6.5).</li>
<li>Política, marco y criterios de riesgo: cada año, en noviembre.</li>
<li>Revisión extraordinaria ante un incidente grave, un sistema o proveedor crítico nuevo, un cambio de ley o de permisos, o un cambio en la distribución de la sala.</li>
<li>ISO 31000 está en proceso de revisión; cuando se publique la nueva edición, el Comité evaluará la transición.</li>
</ul>
</section>"""


def sec_analisis():
    filas = "".join(
        f"<tr><td class='c'><b>{r['id']}</b></td><td>{e(r['nombre'])}</td><td class='c'>{r['fuente']}</td>"
        f"<td class='c'>{r['categoria']}</td><td class='c'>{r['prob']}</td><td class='c'>{r['imp']}</td>"
        f"<td class='c'>{badge(r['nivel'])}</td><td class='c'>{r['estrategia']}</td><td>{e(r['responsable'])}</td></tr>"
        for r in D.RIESGOS)
    cards = []
    for r in D.RIESGOS:
        cards.append(f"""
<div class="risk" style="--tint:#{D.TINTE[r['nivel']]}">
  <div class="risk-hd"><span class="rid">{r['id']}</span><span class="rname">{e(r['nombre'])}</span>{badge(r['nivel'])}</div>
  <table class="risk-t">
    <tr><th>Activo afectado</th><td colspan="3">{e(r['activo'])}</td></tr>
    <tr><th>Amenaza</th><td colspan="3">{e(r['amenaza'])}</td></tr>
    <tr><th>Vulnerabilidad</th><td colspan="3">{e(r['vulnerabilidad'])}</td></tr>
    <tr><th>Fuente</th><td>{r['fuente']}</td><th>Categoría</th><td>{r['categoria']}</td></tr>
    <tr><th>Probabilidad / Impacto</th><td>{r['prob']} / {r['imp']}</td><th>Nivel</th><td><b>{r['nivel']}</b></td></tr>
    <tr><th>Justificación</th><td colspan="3">{e(r['justificacion'])}</td></tr>
    <tr><th>Estrategia</th><td colspan="3"><b>{r['estrategia']}</b></td></tr>
    <tr><th>Plan de respuesta</th><td colspan="3"><ol class="acc">{''.join(f'<li>{e(a)}</li>' for a in r['acciones'])}</ol></td></tr>
    <tr><th>Responsable</th><td>{e(r['responsable'])}</td><th>Tiempos</th><td>{e(r['tiempo'])}</td></tr>
    <tr><th>Recursos</th><td colspan="3">{e(r['recursos'])}</td></tr>
  </table>
</div>""")
    est = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td><td class='c'>{', '.join(r['id'] for r in D.RIESGOS if r['estrategia']==a)}</td></tr>" for a, b in D.ESTRATEGIAS)
    return f"""
<section class="page">
{h(1, "s4", "4. Análisis de riesgos")}
<p>Se identificaron 12 riesgos: los seis de la matriz de riesgos del 10 de octubre de 2026 (R1 a R6) y seis riesgos propios de TI (R7 a R12). Cada uno se describe por el activo afectado, la amenaza y la vulnerabilidad que la amenaza aprovecha.</p>
{h(2, "s4-1", "4.1 Resumen de riesgos")}
<table class="grid small summary"><colgroup><col style="width:5%"><col style="width:25%"><col style="width:8%"><col style="width:11%"><col style="width:7%"><col style="width:8%"><col style="width:10%"><col style="width:9%"><col style="width:17%"></colgroup><thead><tr><th>ID</th><th>Riesgo</th><th>Fuente</th><th>Categoría</th><th>Prob.</th><th>Impacto</th><th>Nivel</th><th>Estrategia</th><th>Responsable</th></tr></thead><tbody>{filas}</tbody></table>
{h(2, "s4-2", "4.2 Estrategias de tratamiento")}
<table class="grid small"><thead><tr><th>Estrategia</th><th>Significado</th><th>Riesgos</th></tr></thead><tbody>{est}</tbody></table>
{h(2, "s4-3", "4.3 Ficha de cada riesgo y plan de respuesta")}
{''.join(cards)}
</section>"""


def sec_mapa():
    por_nivel = {n: [r for r in D.RIESGOS if r["nivel"] == n] for n in D.NIVELES}
    lista = lambda n: "; ".join(f"{r['id']} ({r['nombre'][0].lower() + r['nombre'][1:]})" for r in por_nivel[n])
    return f"""
<section class="page">
{h(1, "s5", "5. Mapa de calor")}
<p>El mapa cruza la probabilidad (eje vertical) con el impacto (eje horizontal). El color de cada celda corresponde al nivel de riesgo según la regla de la sección 3.4, y dentro de cada celda aparecen los ID de los riesgos que caen ahí.</p>
<figure class="fig heat">{heatmap_svg()}<figcaption>Figura 2. Mapa de calor de los 12 riesgos de {e(D.EMPRESA)}.</figcaption></figure>
{h(2, "s5-1", "5.1 Lectura del mapa")}
<ul>
<li><b>Crítico:</b> {e(lista("Crítico"))}. Es la prioridad número uno; sus acciones arrancan en los primeros 30 días y se revisa cada semana.</li>
<li><b>Alto:</b> {e(lista("Alto"))}. Requieren planes de respuesta en un plazo de 30 a 120 días y revisión quincenal.</li>
<li><b>Moderado:</b> {e(lista("Moderado"))}. Se atienden con controles de costo razonable y revisión mensual.</li>
<li><b>Bajo:</b> {e(lista("Bajo"))}. Se acepta con los controles actuales y se revisa cada trimestre.</li>
</ul>
<p>Siete de los doce riesgos están en la columna de impacto Alto: si ocurren, afectan de forma directa el dinero, la ley o la confianza de los clientes. Por eso el plan da prioridad a controles preventivos. También hay riesgos que se encadenan: una falla de respaldos (R11) convierte un ransomware (R7) en una interrupción larga, y el uso de USB (R12) puede ser la puerta de entrada de R7 y R10. La meta del primer año es pasar de 6 a 3 riesgos en nivel Crítico o Alto.</p>
</section>"""


def sec_monitoreo():
    kk = "".join(
        f"<tr><td class='c'><b>{rid}</b><br>{badge(D.RIESGO[rid]['nivel'])}</td><td>{e(D.RIESGO[rid]['nombre'])}</td><td>{e(k['control'])}</td>"
        f"<td>{e(k['kpi'])}<br><span class='meta'>Meta: {e(k['meta'])}</span></td>"
        f"<td>{e(k['kri'])}<br><span class='meta'>Umbral: {e(k['umbral'])}</span></td>"
        f"<td>{e(k['interpretacion'])}</td><td>{e(k['accion'])}</td></tr>"
        for rid, k in D.KPI_KRI.items())
    freq = "".join(
        f"<tr><td class='c'>{badge(n)}</td><td class='c'><b>{D.FRECUENCIA_MONITOREO[n]}</b></td>"
        f"<td class='c'>{', '.join(r['id'] for r in D.RIESGOS if r['nivel']==n)}</td><td>{e(x)}</td></tr>"
        for n, x in [
            ("Crítico", "Reunión semanal del CISO y el Director de TI; alertas de seguridad revisadas a diario."),
            ("Alto", "Revisión quincenal del dueño de riesgo con el equipo de gestión de riesgos."),
            ("Moderado", "Revisión mensual en el Comité de Riesgos."),
            ("Bajo", "Revisión trimestral para confirmar que la aceptación sigue siendo válida."),
        ])
    return f"""
<section class="page">
{h(1, "s6", "6. Monitoreo y control")}
{h(2, "s6-1", "6.1 Objetivos")}
<ul>
<li>Asegurar que los riesgos se gestionen eficazmente a lo largo del tiempo.</li>
<li>Detectar cambios en los riesgos existentes o la aparición de riesgos nuevos.</li>
<li>Evaluar si las medidas de tratamiento están funcionando y corregirlas a tiempo.</li>
</ul>
{h(2, "s6-2", "6.2 Qué se monitorea")}
<ul>
<li><b>Riesgos existentes:</b> si su probabilidad o impacto cambió y si se mueven en el mapa de calor.</li>
<li><b>Eficacia de los controles:</b> con los KPI de cada riesgo.</li>
<li><b>Nivel de exposición:</b> con los KRI y sus umbrales.</li>
<li><b>Avance de los planes de respuesta:</b> acciones terminadas contra lo comprometido.</li>
<li><b>Riesgos nuevos:</b> por sistemas o proveedores nuevos, cambios de ley o amenazas recientes.</li>
<li><b>Incidentes y casi incidentes:</b> registrados en la bitácora única.</li>
<li><b>Riesgos aceptados:</b> que R4 siga siendo Bajo.</li>
</ul>
{h(2, "s6-3", "6.3 Herramientas y técnicas de monitoreo")}
<table class="kv">
<tr><th>Matriz de seguimiento</th><td>Archivo de Excel con los 12 riesgos, su nivel, estrategia, responsable y avance.</td></tr>
<tr><th>Indicadores de riesgo</th><td>Tablero de KPI y KRI con semáforo: verde si el KPI cumple la meta y el KRI está bajo el umbral; amarillo si uno falla; rojo si fallan los dos.</td></tr>
<tr><th>Alertas de sistemas</th><td>Alertas del SIEM, del antimalware avanzado (EDR), de pérdida de señal de cámaras, de reglas de caja y del módulo PLD.</td></tr>
<tr><th>Reuniones periódicas</th><td>Revisiones de dueños de riesgo y del Comité de Riesgos según la frecuencia de la sección 6.5.</td></tr>
<tr><th>Auditorías</th><td>Auditoría Interna revisa cada semestre una muestra de controles; auditoría PLD independiente cada año.</td></tr>
<tr><th>Pruebas y simulacros</th><td>Simulacros de phishing, pruebas de restauración de respaldos y prueba de contingencia de pagos.</td></tr>
<tr><th>Registro de incidentes</th><td>Bitácora única para TI, vigilancia, caja y juego, base para recalcular probabilidades.</td></tr>
</table>
{h(2, "s6-4", "6.4 Tablero de KPI y KRI por riesgo")}
<p>Los riesgos R1, R2 y R5 se retoman de la actividad de KPI y KRI del 18 de octubre de 2026. Se corrigió el KRI de R1 (“# de inconsistencias”) y en R2 se usa el término “cajeros” tanto en el control como en el KPI. Los demás riesgos tienen indicadores nuevos.</p>
<table class="grid xsmall kk"><colgroup><col style="width:8%"><col style="width:12%"><col style="width:14%"><col style="width:17%"><col style="width:17%"><col style="width:16%"><col style="width:16%"></colgroup><thead><tr><th>ID</th><th>Riesgo</th><th>Control</th><th>KPI (desempeño del control)</th><th>KRI (nivel del riesgo)</th><th>Interpretación</th><th>Acción</th></tr></thead><tbody>{kk}</tbody></table>
{h(2, "s6-5", "6.5 Frecuencia de monitoreo por nivel de riesgo")}
<table class="grid small"><thead><tr><th>Nivel</th><th>Frecuencia</th><th>Riesgos</th><th>Cómo se revisa</th></tr></thead><tbody>{freq}</tbody></table>
<p>Además, la matriz completa se revisa cada trimestre y el marco de gestión de riesgos cada año.</p>
{h(2, "s6-6", "6.6 Documentación y reporte")}
<ul>
<li><b>Matriz de riesgos</b> en Excel con control de versiones; cada cambio de nivel queda registrado con fecha y motivo.</li>
<li><b>Ficha de seguimiento</b> por riesgo con evidencia de las acciones terminadas.</li>
<li><b>Bitácora de incidentes</b> con fecha, causa, impacto y acciones.</li>
<li><b>Actas del Comité de Riesgos</b> con acuerdos y responsables.</li>
<li><b>Reporte mensual</b> al Comité: mapa de calor, riesgos que cambiaron de nivel, semáforo de KPI y KRI y acciones vencidas.</li>
<li><b>Informe trimestral</b> a la Dirección General con el resumen ejecutivo y las decisiones requeridas.</li>
<li>Las evidencias se conservan según la política de retención de la empresa y los plazos legales aplicables.</li>
</ul>
{h(2, "s6-7", "6.7 Beneficios del monitoreo y control")}
<ul>
<li>Permite responder rápido ante incidentes porque las alertas llegan a un responsable definido.</li>
<li>Muestra con datos si una inversión en controles está funcionando.</li>
<li>Detecta riesgos nuevos antes de que se conviertan en pérdidas.</li>
<li>Da evidencia ante auditorías y autoridades.</li>
<li>Ayuda a decidir dónde invertir primero.</li>
</ul>
</section>"""


def sec_comunicacion():
    tabla = "".join(f"<tr><td><b>{e(a)}</b></td><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td><td>{e(f)}</td></tr>"
                    for a, b, c, d, f in D.COMUNICACION)
    canales = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in D.CANALES)
    return f"""
<section class="page">
{h(1, "s7", "7. Comunicación")}
{h(2, "s7-1", "7.1 Qué se comunica")}
<ul>
<li>Riesgos identificados, su nivel y su responsable.</li>
<li>Cambios de nivel y aparición de riesgos nuevos.</li>
<li>Avance de los planes de respuesta y valores de KPI y KRI.</li>
<li>Incidentes, sus causas y lecciones aprendidas.</li>
<li>Recomendaciones y decisiones que debe tomar la dirección.</li>
<li>Buenas prácticas para todo el personal (por ejemplo, cómo reconocer un correo de phishing).</li>
</ul>
{h(2, "s7-2", "7.2 Quién comunica y quién recibe")}
<p>Los <b>responsables de riesgos</b> (dueños de cada riesgo, como el CISO, el Gerente de Caja y Tesorería o el Jefe de Vigilancia) informan el estado de su riesgo. El <b>equipo de gestión de riesgos</b>, encabezado por el Gerente de Riesgos y Cumplimiento, reúne la información y la difunde al Comité, a la dirección y al personal.</p>
<table class="grid small"><thead><tr><th>Quién comunica</th><th>Quién recibe</th><th>Qué</th><th>Canal</th><th>Frecuencia</th></tr></thead><tbody>{tabla}</tbody></table>
{h(2, "s7-3", "7.3 Canales de comunicación")}
<table class="kv">{canales}</table>
{h(2, "s7-4", "7.4 Frecuencia de comunicación")}
<ul>
<li><b>Inmediata:</b> incidentes graves o riesgos que pasan a nivel Crítico (menos de 1 hora).</li>
<li><b>Semanal:</b> seguimiento de riesgos críticos.</li>
<li><b>Quincenal:</b> seguimiento de riesgos altos.</li>
<li><b>Mensual:</b> Comité de Riesgos, riesgos moderados y boletín de seguridad al personal.</li>
<li><b>Trimestral:</b> informe a la Dirección General y revisión de riesgos bajos.</li>
<li><b>Anual:</b> revisión del plan completo y capacitación general.</li>
</ul>
</section>"""


def sec_conclusion():
    return f"""
<section class="page">
{h(1, "s8", "8. Conclusión")}
<p>Para {e(D.EMPRESA)} la tecnología sostiene el negocio: sin sistemas no hay caja, sin cámaras no hay control de la sala y sin datos confiables no hay programa de lealtad ni cumplimiento ante la autoridad. El plan identificó 12 riesgos, de los cuales uno es Crítico (ransomware) y cinco son Altos. Todos tienen un responsable, una estrategia, acciones con plazo y un par de indicadores para saber si el control funciona.</p>
<p><b>Importancia de la mejora continua.</b> Los riesgos cambian: aparecen nuevas formas de ataque, se cambian sistemas y proveedores, y las leyes se reforman. Por eso el plan no termina con la matriz. El ciclo de ISO 31000 obliga a medir, revisar y ajustar: la matriz se actualiza cada trimestre, los indicadores según el nivel de cada riesgo y el marco completo cada año. Cada incidente debe dejar una lección y un ajuste en los controles.</p>
<p><b>Cultura organizacional orientada a la gestión de riesgos.</b> Los controles técnicos no bastan si el personal no los aplica. Un cajero que rota de ventanilla, un crupier que registra la inspección de la baraja o un empleado que reporta un correo sospechoso reducen el riesgo tanto como una herramienta de seguridad. La dirección debe dar el ejemplo, reconocer a quien reporta y tratar los errores como oportunidades de mejora, no como motivo de castigo. Con esa cultura, la gestión de riesgos deja de ser un documento y se vuelve parte del trabajo diario del casino.</p>
</section>"""


def sec_referencias():
    refs = "".join(f"<p class='ref'>{r}</p>" for r in D.REFERENCIAS)
    return f"""
<section class="page">
{h(1, "refs", "Referencias")}
{refs}
</section>"""


CSS = open(os.path.join(HERE, "doc.css"), encoding="utf-8").read()


def build_html(pages):
    TOC.clear()
    body_secs = [sec_empresa(), sec_intro(), sec_metodologia(), sec_analisis(), sec_mapa(),
                 sec_monitoreo(), sec_comunicacion(), sec_conclusion(), sec_referencias()]
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<title>PIA {e(D.TITULO)} - {e(D.EMPRESA)}</title><style>{CSS}</style></head><body>
{portada()}{indice(pages)}{''.join(body_secs)}</body></html>"""
    return doc


def render_pdf(html_path, pdf_path):
    subprocess.run(["node", os.path.join(HERE, "render.js"), "pdf", html_path, pdf_path], check=True)


def outline_pages(pdf_path):
    r = PdfReader(pdf_path)
    res = {}

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                t = it.title.strip()
                if len(t) % 2 == 0 and t[:len(t) // 2] == t[len(t) // 2:]:
                    t = t[:len(t) // 2]  # Chromium duplica el texto de algunos h1
                res.setdefault(t, r.get_destination_page_number(it) + 1)
    walk(r.outline)
    return res


def stamp(pdf_in, pdf_out):
    pdfmetrics.registerFont(TTFont("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"))
    reader = PdfReader(pdf_in)
    writer = PdfWriter(clone_from=reader)
    for i, page in enumerate(writer.pages):
        if i == 0:
            continue
        w = float(page.mediabox.width)
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(w, float(page.mediabox.height)))
        c.setFont("LibSans", 8)
        c.setFillColorRGB(0.36, 0.39, 0.46)
        c.drawString(56.7, 28, f"{D.EMPRESA} · PIA {D.MATERIA} · Grupo {D.GRUPO}")
        c.drawRightString(w - 56.7, 28, f"Página {i + 1} de {len(writer.pages)}")
        c.save()
        buf.seek(0)
        page.merge_page(PdfReader(buf).pages[0])
    writer.add_metadata({"/Title": f"PIA - {D.TITULO} - {D.EMPRESA}",
                         "/Author": ", ".join(n for n, _ in D.INTEGRANTES),
                         "/Subject": f"{D.MATERIA}, grupo {D.GRUPO}"})
    writer.write(pdf_out)


def main():
    html_path = os.path.join(BUILD, "documento.html")
    tmp_pdf = os.path.join(BUILD, "documento_tmp.pdf")
    pages = {}
    for _ in range(3):
        open(html_path, "w", encoding="utf-8").write(build_html(pages))
        render_pdf(html_path, tmp_pdf)
        found = outline_pages(tmp_pdf)
        new = {}
        for level, hid, text in TOC:
            if text not in found:
                sys.exit(f"No se encontró en el PDF el encabezado: {text}")
            new[hid] = found[text]
        if new == pages:
            break
        pages = new
    else:
        sys.exit("El índice no se estabilizó")
    json.dump({t: pages[h_] for _, h_, t in TOC}, open(os.path.join(BUILD, "indice.json"), "w"), ensure_ascii=False, indent=1)
    final = os.path.join(OUT, "PIA_061_Casino_Royale_Administracion_de_Riesgos_TI.pdf")
    stamp(tmp_pdf, final)
    print("PDF:", final, "páginas:", len(PdfReader(final).pages))


if __name__ == "__main__":
    main()
