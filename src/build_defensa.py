# -*- coding: utf-8 -*-
"""Guía de defensa del plan (documento de apoyo para el equipo, no es entregable
del PIA). Explica por qué se eligió cada parte, mejoras a futuro y posibles
puntos de falla. Las páginas citadas salen de build/indice.json, que genera
build_doc.py, para que coincidan siempre con el PDF del PIA."""
import json
import os

import data as D
from build_doc import BUILD, render_pdf, stamp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
APOYO = os.path.join(ROOT, "apoyo")
os.makedirs(APOYO, exist_ok=True)
FINAL = os.path.join(APOYO, "Guia_de_defensa_del_plan.pdf")

IDX = json.load(open(os.path.join(BUILD, "indice.json"), encoding="utf-8"))
SECCIONES = [k for k in IDX if k[0].isdigit() and k.split(" ")[0].endswith(".") or k == "Referencias"]


def pag(clave):
    """Página o rango de páginas de una sección o subsección del PIA."""
    claves = list(IDX)
    ini = IDX[clave]
    if clave in SECCIONES:
        k = SECCIONES.index(clave)
        fin = IDX[SECCIONES[k + 1]] - 1 if k + 1 < len(SECCIONES) else ini
        # si la sección siguiente empieza a media página, la anterior termina ahí
        fin = max(ini, fin)
        return f"pág. {ini}" if fin == ini else f"págs. {ini}–{fin}"
    return f"pág. {ini}"


def p(clave):
    return f'<span class="pg">{pag(clave)}</span>'


cuenta = lambda campo, valor: sum(1 for r in D.RIESGOS if r[campo] == valor)
N_MIT = cuenta("estrategia", "Mitigar")
N_TEC = cuenta("categoria", "Tecnológico")

S1 = "1. Descripción de la empresa y del área de TI"
S2 = "2. Introducción"
S3 = "3. Metodología"
S4 = "4. Análisis de riesgos"
S5 = "5. Mapa de calor"
S6 = "6. Monitoreo y control"
S7 = "7. Comunicación"
S8 = "8. Conclusión"

HTML = f"""
<header>
  <div class="kicker">Documento de apoyo para el equipo · Grupo {D.GRUPO}</div>
  <h1>Guía de defensa del plan</h1>
  <div class="lead">Por qué elegimos cada parte del plan de {D.EMPRESA}, qué mejoras y alternativas tiene a futuro y dónde podría fallar</div>
</header>
<p class="note">Esta guía no es parte de los entregables. Sirve para preparar la exposición y las preguntas del docente. Las páginas citadas corresponden al documento del PIA.</p>

<h2 class="nobreak">Ideas clave para defender el plan</h2>
<ol class="clave">
<li><b>Un solo método para todo el casino.</b> ISO 31000 permite medir con la misma regla un fraude en mesas, el lavado de dinero y un ransomware.</li>
<li><b>Cada riesgo apunta a una vulnerabilidad concreta.</b> Por eso cada control tiene sentido: ataca la causa, no el síntoma.</li>
<li><b>La estrategia depende del riesgo, no de una costumbre.</b> Mitigamos lo que es parte del negocio, transferimos lo que depende de un tercero, evitamos lo que no aporta valor y aceptamos lo que ya está controlado.</li>
<li><b>Medimos con dos indicadores por riesgo.</b> El KPI dice si el control se aplica y el KRI si la exposición baja. Uno solo puede engañar.</li>
<li><b>El plan reconoce sus límites.</b> Los datos de partida son estimaciones y por eso se revisa cada trimestre.</li>
</ol>

<section class="parte">
<h2>1. Descripción de la empresa y del área de TI {p(S1)}</h2>
<div class="bloque"><div class="lbl">Por qué la incluimos</div>
<p>ISO 31000 pide definir el contexto antes de buscar riesgos. Además, cada sistema que describimos aparece después como un activo afectado en el análisis: el CRM corresponde a R4, la red con VLAN a R7 y el enlace único de pagos a R8.</p></div>
<div class="bloque"><div class="lbl">Cómo se hizo</div>
<p>Como es un caso ficticio, la misión, la visión, los sistemas y la ubicación son supuestos, y el documento lo aclara al inicio de la sección.</p></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<p>En una empresa real esto sería un inventario de activos con su nivel de importancia, diagramas de red y un análisis de impacto al negocio (BIA): cuánto cuesta cada hora sin cada sistema. Ese dato haría mucho más precisa la medición del impacto.</p></div>
</section>

<section class="parte">
<h2>2. Introducción: objetivo, alcance, responsables y KPI/KRI {p(S2)}</h2>
<div class="bloque"><div class="lbl">Por qué ese alcance</div>
<p>Incluimos TI y también los procesos que dependen de ella: juego, caja, cámaras, programa de lealtad y cumplimiento legal. En un casino casi todos los riesgos operativos pasan por un sistema; por eso los riesgos de la matriz anterior (R1 a R6) caben en un plan de TI. Dejamos fuera construcción y protección civil porque no involucran tecnología.</p></div>
<div class="bloque"><div class="lbl">Por qué esa estructura de responsables</div>
<ul>
<li>Cada riesgo tiene un dueño, que es quien controla el proceso (Caja, Juego, Vigilancia, TI).</li>
<li>Un equipo de riesgos coordina el plan.</li>
<li>Auditoría Interna revisa de forma independiente.</li>
</ul>
<p>Así quien opera el control no es quien lo evalúa. Por eso no todos los riesgos son de TI: R2 es de Tesorería y R6 del Oficial de Cumplimiento.</p></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<ul>
<li>Una tabla RACI que diga quién ejecuta, quién aprueba, a quién se consulta y a quién se informa.</li>
<li>Una declaración formal de <b>apetito de riesgo</b>: cuánto riesgo acepta la dirección. Hoy el plan no la tiene (punto de falla 2).</li>
</ul></div>
</section>

<section class="parte">
<h2>3. Metodología {p(S3)}</h2>
<h3>ISO 31000 como estándar {p("3.1 Estándar: ISO 31000:2018")}</h3>
<div class="bloque"><div class="lbl">Por qué</div>
<p>Sirve para cualquier tipo de riesgo, no solo de ciberseguridad. Eso nos permitió poner en una sola matriz el fraude en mesas, el lavado de dinero y el ransomware. También da un lenguaje común para áreas que antes tenían listas de riesgos separadas (reto «Áreas separadas»).</p></div>
<div class="bloque fut"><div class="lbl">Alternativas que se pueden sumar a futuro</div>
<table class="grid">
<thead><tr><th>Marco</th><th>Cuándo convendría</th></tr></thead><tbody>
<tr><td><b>ISO/IEC 27001 y 27002</b></td><td>Si el casino quiere una <b>certificación</b>, porque ISO 31000 no se certifica. También da un catálogo de controles concretos.</td></tr>
<tr><td><b>NIST CSF</b></td><td>Para madurar la parte de ciberseguridad (R7, R9, R10 y R12).</td></tr>
<tr><td><b>PCI DSS</b></td><td>Si el casino procesa o guarda datos de tarjetas. Las terminales de pago de R8 lo harían relevante.</td></tr>
<tr><td><b>ISO 22301</b></td><td>Para un plan formal de continuidad del negocio, que hoy solo existe implícito en R8 y R11.</td></tr>
<tr><td><b>COSO ERM</b></td><td>Si la dirección quiere integrar el riesgo con la estrategia y la auditoría financiera.</td></tr>
</tbody></table>
<p>Además, ISO 31000 está en revisión. El plan ya prevé evaluar la transición cuando salga la nueva edición ({pag("3.5 Implementación de ISO 31000 en el casino (caso simulado)")}).</p></div>

<h3>Herramientas de identificación {p("3.2 Herramientas de identificación y análisis")}</h3>
<div class="bloque"><div class="lbl">Por qué esa combinación</div>
<p>Cada herramienta cubre un punto ciego de las otras:</p>
<ul>
<li><b>Encuestas anónimas:</b> el personal operativo habla sin miedo. Así salieron R5, R12 y las cuentas compartidas de R9.</li>
<li><b>Entrevistas:</b> dan profundidad con los responsables de cada área.</li>
<li><b>Lluvia de ideas:</b> el Comité propone riesgos sin juzgarlos. Así salieron R7, R8, R10 y R11.</li>
<li><b>FODA:</b> convierte debilidades internas en riesgos concretos cuando se cruzan con una amenaza.</li>
</ul></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<p>El FODA es más estratégico que técnico. Se puede complementar con el análisis de corbatín (bow-tie: causas, evento y consecuencias, útil para R7), ejercicios de mesa que simulan un incidente, pruebas de penetración y revisión de bitácoras reales. Con eso las probabilidades dejan de depender solo de opiniones.</p></div>

<h3>Clasificación en cinco categorías {p("3.3 Clasificación de riesgos")}</h3>
<div class="bloque"><div class="lbl">Por qué</div>
<p>La pide el PIA y ayuda a ver dónde se concentra la exposición: {N_TEC} de 12 riesgos son tecnológicos.</p></div>
<div class="bloque fut"><div class="lbl">Limitación y mejora</div>
<p>Cada riesgo tiene una sola categoría, pero varios son mixtos: R10 es reputacional y también legal. Conviene usar una categoría principal y otra secundaria.</p></div>

<h3>Escala 3x3 y regla del nivel {p("3.4 Criterios de valoración")}</h3>
<div class="bloque"><div class="lbl">Por qué</div>
<p>La pide el PIA y la entiende cualquier persona sin conocimientos técnicos. Definimos una tabla de conversión desde la matriz 5x5 anterior para no perder el trabajo previo.</p></div>
<div class="bloque"><div class="lbl">Costo de simplificar</div>
<ul>
<li>R3 bajó de Alto a Moderado solo por el cambio de escala.</li>
<li>Cuatro riesgos quedaron en la misma celda (Media/Alto) sin forma de distinguir cuál es más urgente.</li>
<li>Los criterios son cualitativos: dicen «pérdidas importantes», pero no cuánto dinero.</li>
</ul></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<ul>
<li>Poner montos en pesos y horas de interrupción en cada nivel de impacto.</li>
<li>Pasar a 5x5 o a un análisis cuantitativo: pérdida anual esperada = pérdida por evento × veces al año, o el método FAIR.</li>
</ul></div>

<h3>Implementación en seis fases {p("3.5 Implementación de ISO 31000 en el casino (caso simulado)")}</h3>
<div class="bloque"><div class="lbl">Por qué en ese orden</div>
<ol>
<li><b>Mandato primero:</b> sin patrocinio de la dirección no hay presupuesto ni prioridad.</li>
<li><b>Marco antes de evaluar:</b> todos tienen que medir con la misma escala.</li>
<li><b>Contexto antes de identificar:</b> no se puede encontrar el riesgo de un sistema que no se ha inventariado.</li>
<li><b>Evaluar, después tratar y después dar seguimiento:</b> es el ciclo del proceso de ISO 31000 (cláusulas 6.3 a 6.7).</li>
</ol>
<p>La comunicación y consulta es transversal porque el estándar la exige durante todo el proceso, no solo al final.</p></div>
<div class="bloque"><div class="lbl">Por qué esa renovación</div>
<p>La matriz se revisa cada trimestre, el marco cada año y hay revisión extraordinaria ante cambios importantes. Así el plan no se vuelve un documento muerto.</p></div>
</section>

<section class="parte">
<h2>4. Análisis de riesgos {p(S4)}</h2>
<div class="bloque"><div class="lbl">Por qué activo, amenaza y vulnerabilidad</div>
<p>Hace que el riesgo se pueda atacar, porque el control siempre va contra la vulnerabilidad. En R9 la vulnerabilidad son las cuentas compartidas, y el control es crear cuentas nominales y usar una herramienta de accesos privilegiados (PAM).</p></div>
<div class="bloque"><div class="lbl">Por qué esos riesgos nuevos de TI (R7 a R12)</div>
<p>Un casino reúne tres cosas atractivas para un atacante: mucho efectivo, datos personales y bancarios, y operación continua donde cada hora parado cuesta. Ransomware, pagos, accesos privilegiados, fuga de datos y respaldos atacan justo esos tres puntos.</p></div>
<div class="bloque"><div class="lbl">Por qué cada estrategia {p("4.2 Estrategias de tratamiento")}</div>
<table class="grid">
<thead><tr><th>Estrategia</th><th>Riesgos</th><th>Razón</th></tr></thead><tbody>
<tr><td><b>Mitigar</b></td><td class="nw">{N_MIT} de 12</td><td>Son actividades del negocio que no se pueden eliminar, como tener caja, mesas o datos. Lo razonable es reducirlas con controles.</td></tr>
<tr><td><b>Transferir</b></td><td>R8</td><td>La falla depende de un tercero (el procesador de pagos). Un contrato con penalizaciones y un seguro trasladan la pérdida económica. Como transferir no evita la caída, agregamos un segundo enlace y un procedimiento manual.</td></tr>
<tr><td><b>Evitar</b></td><td>R12</td><td>Usar USB y programas no autorizados no le aporta nada al negocio. Prohibirlo cuesta menos que controlarlo.</td></tr>
<tr><td><b>Aceptar</b></td><td>R4</td><td>Es Bajo y ya tiene firewall de aplicaciones y doble factor. Agregar más controles costaría más de lo que reduce. Se vigila cada trimestre.</td></tr>
</tbody></table></div>
<div class="bloque"><div class="lbl">Por qué esos plazos</div>
<p>Van de 15 a 120 días y siguen el nivel: primero lo Crítico y lo barato (doble factor, EDR, rotación de cajeros), y después lo que requiere compras o proyectos (PAM, DLP, sensores).</p></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<ul>
<li><b>Calcular el riesgo residual</b>, es decir, el nivel esperado después del tratamiento. Hoy solo está el riesgo inherente.</li>
<li>Poner costo a cada plan de respuesta.</li>
<li>Ligar cada control a un catálogo estándar, como ISO/IEC 27002.</li>
<li>Agregar los riesgos que faltan (punto de falla 7).</li>
</ul></div>
</section>

<section class="parte">
<h2>5. Mapa de calor {p(S5)}</h2>
<div class="bloque"><div class="lbl">Por qué</div>
<p>Resume los 12 riesgos en una imagen que la dirección entiende en segundos. Lo usamos para priorizar cuando el presupuesto no alcanzaba (reto «Presupuesto limitado»). La meta de pasar de 6 a 3 riesgos Crítico o Alto da un objetivo medible.</p></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<ul>
<li>Dos mapas lado a lado, antes y después del tratamiento, para mostrar el avance.</li>
<li>Su evolución trimestre a trimestre.</li>
<li>Mostrar las dependencias entre riesgos, que hoy solo se explican en texto: R11 agrava R7 y R12 puede ser la puerta de entrada de R7.</li>
</ul></div>
</section>

<section class="parte">
<h2>6. Monitoreo y control {p(S6)}</h2>
<div class="bloque"><div class="lbl">Por qué un KPI y un KRI por riesgo {p("6.4 Tablero de KPI y KRI por riesgo")}</div>
<p>Uno solo engaña. En R2 la rotación de cajeros puede cumplirse al 100 % (KPI en verde) mientras las transacciones sospechosas suben (KRI en rojo): el control no basta. Leídos juntos dicen si el control realmente reduce el riesgo.</p></div>
<div class="bloque"><div class="lbl">Por qué la frecuencia según el nivel {p("6.5 Frecuencia de monitoreo por nivel de riesgo")}</div>
<p>El tiempo del equipo se reparte según el riesgo. No tiene sentido revisar R4 cada semana y R7 cada trimestre.</p></div>
<div class="bloque"><div class="lbl">Por qué esas herramientas {p("6.3 Herramientas y técnicas de monitoreo")}</div>
<ul>
<li><b>Alertas de sistemas</b> (SIEM, EDR, cámaras, módulo PLD): detectan en tiempo real.</li>
<li><b>Reuniones:</b> sirven para decidir.</li>
<li><b>Auditorías:</b> dan una revisión independiente.</li>
<li><b>Simulacros:</b> prueban que el control funciona de verdad. Un respaldo que nunca se restauró no está probado.</li>
</ul></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<ul>
<li>Muchos KRI son <b>de rezago</b>: cuentan incidentes que ya pasaron. Conviene agregar KRI <b>anticipados</b>, como equipos sin parche, vulnerabilidades abiertas o rotación de personal.</li>
<li>Los umbrales (más de 3 al mes, más de 5 %) son supuestos. Hay que ajustarlos con una línea base real de 3 a 6 meses.</li>
<li>Automatizar el tablero con un sistema de gobierno, riesgo y cumplimiento (GRC) conectado a los sistemas.</li>
<li>Precisar la redacción de algunos KRI: R12 dice «aumento 2 meses seguidos» y R4 «+50 % sobre el promedio» sin definir de qué periodo es el promedio.</li>
</ul></div>
</section>

<section class="parte">
<h2>7. Comunicación {p(S7)}</h2>
<div class="bloque"><div class="lbl">Por qué así</div>
<p>La tabla de quién comunica a quién evita que un incidente se quede en un área: los dueños reportan al equipo de riesgos, el equipo al Comité y el Comité a la dirección. El aviso en menos de 1 hora para incidentes graves existe porque en un ransomware cada hora cuenta. Incluimos comunicación externa (avisos a la autoridad y a clientes afectados) porque la ley antilavado y la de protección de datos personales lo hacen necesario.</p></div>
<div class="bloque fut"><div class="lbl">A futuro</div>
<p>Un plan de comunicación de crisis con vocero designado, plantillas de mensajes y simulacros, y medir la cultura de reporte: cuántos reportes hace el personal y cuánto tardan.</p></div>
</section>

<section class="parte">
<h2>8. Conclusión {p(S8)}</h2>
<div class="bloque"><div class="lbl">Por qué esos dos temas</div>
<p>Los pide el PIA y además son la razón de fondo de todo lo anterior:</p>
<ul>
<li><b>Mejora continua:</b> los riesgos cambian, y el plan tiene que cambiar con ellos.</li>
<li><b>Cultura:</b> la mayoría de los controles dependen de personas: el cajero que rota, el crupier que revisa la baraja o el empleado que reporta un correo sospechoso.</li>
</ul></div>
</section>

<section class="parte fallas-sec">
<h2>Posibles puntos de falla del plan</h2>
<p>Estos son los puntos donde el docente podría cuestionar el plan, o donde fallaría en una empresa real, con la forma de corregirlos.</p>
<table class="grid fallas">
<thead><tr><th>#</th><th>Punto de falla</th><th>Por qué es un riesgo para el plan</th><th>Cómo corregirlo</th></tr></thead><tbody>
<tr><td class="c">1</td><td><b>Probabilidades e impactos subjetivos</b></td><td>Salieron de talleres y encuestas, sin historial, porque no había bitácora de incidentes (reto «Datos incompletos»). Puede haber sesgo.</td><td>Usar la bitácora nueva y recalificar cada trimestre con datos reales.</td></tr>
<tr><td class="c">2</td><td><b>Sin apetito de riesgo ni criterios en pesos</b></td><td>Decisiones como aceptar R4 se pueden discutir porque no hay un límite formal.</td><td>Que la dirección firme cuánto riesgo acepta y qué montos definen cada nivel de impacto.</td></tr>
<tr><td class="c">3</td><td><b>Sin riesgo residual ni costos</b></td><td>No se demuestra que la meta de pasar de 6 a 3 sea alcanzable ni que valga lo que cuesta.</td><td>Calcular el nivel después del tratamiento y el presupuesto de cada plan.</td></tr>
<tr><td class="c">4</td><td><b>Presupuesto no asegurado</b></td><td>Los planes dependen de licencias (EDR, PAM, DLP) y de un seguro que no tienen monto aprobado.</td><td>Llevar los montos al Comité, ordenados por nivel de riesgo.</td></tr>
<tr><td class="c">5</td><td><b>Carga concentrada</b></td><td>El CISO es dueño de R7 y R9 y apoya R10. A 30 días coinciden doble factor, EDR, bloqueo de USB y alertas, casi todo para el mismo equipo de TI.</td><td>Escalonar plazos, apoyarse en proveedores o nombrar suplentes por riesgo.</td></tr>
<tr><td class="c">6</td><td><b>Dependencia de personas</b></td><td>La rotación, las inspecciones manuales y el reporte de incidentes fallan si la cultura no cambia (reto «Resistencia del personal»).</td><td>Capacitación continua, reconocer a quien reporta y automatizar donde se pueda.</td></tr>
<tr><td class="c">7</td><td><b>Riesgos no considerados</b></td><td>Hay huecos fuera de la matriz (lista abajo).</td><td>Incluirlos en la próxima revisión trimestral.</td></tr>
<tr><td class="c">8</td><td><b>Riesgos encadenados</b></td><td>Si R11 falla, R7 pasa de incidente a desastre. El mapa los trata por separado.</td><td>Escenarios combinados y un plan de recuperación (DRP) con RTO y RPO probados.</td></tr>
<tr><td class="c">9</td><td><b>KRI con umbrales sin base</b></td><td>Pueden dar falsas alarmas o dejar pasar un problema real.</td><td>Medir de 3 a 6 meses antes de fijar umbrales definitivos.</td></tr>
<tr><td class="c">10</td><td><b>Sin plan formal de continuidad</b></td><td>Solo R8 y R11 hablan de recuperación, y hay una sola sala sin sitio alterno.</td><td>Plan de continuidad del negocio (BCP/DRP) basado en ISO 22301.</td></tr>
<tr><td class="c">11</td><td><b>Cambios regulatorios</b></td><td>La ley antilavado se reformó en 2025. Si cambia de nuevo, los controles de R6 pueden quedar desactualizados.</td><td>Revisión de cambios legales con asesoría externa como tarea fija, no solo extraordinaria.</td></tr>
<tr><td class="c">12</td><td><b>Sin validación externa</b></td><td>ISO 31000 no se certifica, así que nadie de fuera confirma que el plan funcione.</td><td>Auditoría externa o, a futuro, certificación ISO/IEC 27001.</td></tr>
</tbody></table>
<div class="bloque fut"><div class="lbl">Riesgos que hoy no están en la matriz (punto 7)</div>
<ul class="cols">
<li>Corte de energía o falla del centro de datos (no hay riesgo de UPS ni de planta eléctrica).</li>
<li>Proveedores críticos, como el fabricante de tragamonedas.</li>
<li>Phishing como riesgo propio; hoy solo aparece como vía de entrada de R7.</li>
<li>Ataques de denegación de servicio (DDoS) al portal de clientes.</li>
<li>PCI DSS para los datos de tarjeta.</li>
<li>Robo físico en la caja.</li>
<li>Juego responsable.</li>
</ul></div>
</section>
"""

CSS = open(os.path.join(HERE, "guion.css"), encoding="utf-8").read() + """
h2 { margin-top: 4pt; }
h2 .pg, h3 .pg, .lbl .pg { font-size: 9.5pt; font-weight: 400; color: var(--muted); margin-left: 6pt;
  text-transform: none; letter-spacing: 0; }
h3 { margin: 12pt 0 6pt; break-after: avoid; }
.parte { break-before: auto; margin-top: 16pt; }
.note { background: var(--soft); border-radius: 6pt; padding: 7pt 10pt; font-size: 10pt; color: var(--muted); }
.bloque { border-left: 0; background: #FFFFFF; border: 0.8pt solid var(--line); border-radius: 7pt;
  padding: 7pt 11pt 3pt; margin: 0 0 8pt; break-inside: avoid; }
.bloque.fut { background: #FBF7EA; border-color: #EADFB8; }
.lbl { font-size: 8.8pt; letter-spacing: 1.1pt; text-transform: uppercase; font-weight: 700; color: var(--gold);
  margin-bottom: 3pt; }
.bloque p, .bloque ul, .bloque ol { margin: 0 0 6pt; }
.bloque ul, .bloque ol { padding-left: 16pt; }
.bloque table { margin: 2pt 0 6pt; font-size: 10.5pt; }
ol.clave { padding-left: 18pt; }
ol.clave li { margin-bottom: 4pt; }
.fallas { font-size: 10pt; }
.fallas tr { break-inside: avoid; }
ul.cols { columns: 2; column-gap: 18pt; }
/* que un título nunca quede solo al final de la página: reserva espacio para lo que sigue */
h2, h3 { break-inside: avoid; }
h2::after, h3::after { content: ""; display: block; height: 150pt; margin-bottom: -150pt; }
.parte.fallas-sec { break-before: page; margin-top: 0; }
"""


def main():
    doc = f"""<!doctype html><html lang="es-MX"><head><meta charset="utf-8">
<title>Guía de defensa del plan - {D.EMPRESA}</title><style>{CSS}</style></head><body>{HTML}</body></html>"""
    path = os.path.join(BUILD, "defensa.html")
    open(path, "w", encoding="utf-8").write(doc)
    tmp = os.path.join(BUILD, "defensa_tmp.pdf")
    render_pdf(path, tmp)
    stamp(tmp, FINAL, title=f"Guía de defensa del plan - {D.EMPRESA}")
    print("Guía de defensa:", FINAL)


if __name__ == "__main__":
    main()
