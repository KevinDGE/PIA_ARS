// Presentación ejecutiva del PIA (12 diapositivas, notas del orador en cada una).
// Los datos de riesgos se leen de build/data.json (generado desde data.py).
const pptxgen = require("pptxgenjs");
const path = require("path");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const BUILD = path.join(ROOT, "build");
const OUT = path.join(ROOT, "entregables", "Presentacion_Ejecutiva_Casino_Royale.pptx");
const SKILL = process.env.PPTX_SKILL;
const D = JSON.parse(fs.readFileSync(path.join(BUILD, "data.json"), "utf8"));
const R = Object.fromEntries(D.RIESGOS.map((r) => [r.id, r]));
if (!Array.isArray(D.NOTAS) || D.NOTAS.length !== 12) throw new Error("Faltan las notas del guion (src/guion.py)");

const THEME = {
  name: "Casino Royale",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F2937", lt1: "FFFFFF", dk2: "0F1F38", lt2: "F3F5F8",
    accent1: "B8901C", accent2: "B71C1C", accent3: "E65100", accent4: "F9A825", accent5: "2E7D32", accent6: "5B6475",
    hlink: "0F1F38", folHlink: "5B6475",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = `${D.TITULO} - ${D.EMPRESA}`;
pres.author = D.INTEGRANTES.map((x) => x[0]).join(", ");
pres.subject = `PIA ${D.MATERIA}, grupo ${D.GRUPO}`;
const C = pres.SchemeColor;
const LVL = { "Crítico": C.accent2, "Alto": C.accent3, "Moderado": C.accent4, "Bajo": C.accent5 };
const LVL_TXT = { "Crítico": C.background1, "Alto": C.background1, "Moderado": C.text1, "Bajo": C.background1 };
const W = 13.333, M = 0.6;
const FOOT = `${D.EMPRESA} · PIA ${D.MATERIA} · Grupo ${D.GRUPO}`;

// ------------------------------------------------------------- layouts
pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 2.45, w: 9.2, h: 1.75, fontSize: 44, bold: true,
                                color: C.background1, valign: "top", align: "left", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: C.background1 },
  margin: [0.4, 0.6, 0.7, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: W - 2 * M, h: 0.85, fontSize: 34, bold: true,
                                color: C.text2, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: M, y: 7.0, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.8, y: 7.0, w: 0.8, h: 0.3, fontSize: 10, color: C.accent6, align: "right" },
});
pres.defineSlideMaster({
  title: "CIERRE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: M, y: 0.35, w: W - 2 * M, h: 0.85, fontSize: 34, bold: true,
                                color: C.background1, valign: "middle", align: "left", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: M, y: 7.0, w: 9, h: 0.3, fontSize: 10, color: "B9C2D3", margin: 0 } } },
  ],
  slideNumber: { x: W - M - 0.8, y: 7.0, w: 0.8, h: 0.3, fontSize: 10, color: "B9C2D3", align: "right" },
});

// ------------------------------------------------------------- utilidades
const img = (n) => path.join(BUILD, n);
const shadow = () => ({ type: "outer", color: "0F1F38", opacity: 0.12, blur: 6, offset: 2, angle: 90 });

function card(slide, x, y, w, h, name, fillColor = C.background2) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: fillColor },
    line: { color: fillColor }, objectName: name });
}
function badge(slide, x, y, d, text, name, fillColor = C.text2, txtColor = C.accent1, fontSize = 18) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fillColor }, line: { color: fillColor }, objectName: name });
  slide.addText(text, { x, y, w: d, h: d, align: "center", valign: "middle", fontSize, bold: true, color: txtColor,
    margin: 0, isTextBox: true, objectName: name + " texto" });
}
function iconCircle(slide, x, y, d, icon, name) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: name });
  const p = d * 0.22;
  slide.addImage({ path: img(`ico_${icon}.png`), x: x + p, y: y + p, w: d - 2 * p, h: d - 2 * p, objectName: name + " icono",
    altText: name });
}
function levelChip(slide, x, y, w, h, nivel, text, name, fontSize = 14) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: h / 2, fill: { color: LVL[nivel] },
    line: { color: LVL[nivel] }, objectName: name });
  slide.addText(text, { x, y, w, h, align: "center", valign: "middle", fontSize, bold: true, color: LVL_TXT[nivel],
    margin: 0, isTextBox: true, objectName: name + " texto" });
}
function content(section, title) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: section });
  s.addText(title, { placeholder: "title" });
  return s;
}

// ------------------------------------------------------------- 1. Portada
pres.addSection({ title: "Introducción" });
{
  const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Introducción" });
  s.addImage({ path: path.join(ROOT, "assets", "logos", "casino_royale_blanco.png"), x: M, y: 0.6, w: 3.1, h: 0.8,
    objectName: "Logo Casino Royale", altText: "Logo de Casino Royale Enterprises" });
  const logos = [["uanl", "Logo UANL"], ["facultad", "Logo de la facultad"]];
  logos.forEach(([stem, label], k) => {
    const x = W - M - 1.9 - (1 - k) * 2.1;
    const f = ["png"].map((e) => path.join(ROOT, "assets", "logos", `${stem}.${e}`)).find((p) => fs.existsSync(p));
    if (f) {
      // respeta la proporción del logo dentro de un espacio de 1.9 x 1.1 in
      const buf = fs.readFileSync(f);
      const iw = buf.readUInt32BE(16), ih = buf.readUInt32BE(20);
      const sc = Math.min(1.9 / iw, 1.1 / ih), w = iw * sc, h = ih * sc;
      s.addImage({ path: f, x: x + (1.9 - w) / 2, y: 0.45 + (1.1 - h) / 2, w, h, objectName: label, altText: label });
    } else {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 0.5, w: 1.9, h: 1.0, rectRadius: 0.08, fill: { color: C.text2 },
        line: { color: "8E9AB0", dashType: "dash", width: 1 }, objectName: `${label} pendiente` });
      s.addText([{ text: label, options: { bold: true, breakLine: true } }, { text: "(pendiente)" }],
        { x, y: 0.5, w: 1.9, h: 1.0, align: "center", valign: "middle", fontSize: 11, color: "B9C2D3", margin: 0,
          isTextBox: true, objectName: `${label} pendiente texto` });
    }
  });
  s.addText(`PIA · ${D.MATERIA.toUpperCase()} · GRUPO ${D.GRUPO}`, { x: M, y: 1.95, w: 10, h: 0.4, fontSize: 14, bold: true,
    color: C.accent1, charSpacing: 2, margin: 0, isTextBox: true, objectName: "Materia" });
  s.addText(D.TITULO, { placeholder: "title" });
  s.addText(`Caso académico: ${D.EMPRESA}`, { x: M, y: 4.2, w: 10, h: 0.5, fontSize: 20, color: "CDD5E3", margin: 0,
    isTextBox: true, objectName: "Subtítulo" });
  const names = D.INTEGRANTES.map(([n, m]) => (m ? `${n} · ${m}` : n));
  s.addText(names.slice(0, 3).map((n, i) => ({ text: n, options: { breakLine: i < 2 } })),
    { x: M, y: 5.3, w: 4.6, h: 1.1, fontSize: 14, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: "Integrantes 1" });
  s.addText(names.slice(3).map((n, i, a) => ({ text: n, options: { breakLine: i < a.length - 1 } })),
    { x: M + 4.7, y: 5.3, w: 4.2, h: 1.1, fontSize: 14, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: "Integrantes 2" });
  s.addText([{ text: "Docente", options: { bold: true, color: C.accent1, breakLine: true } },
             { text: D.DOCENTE, options: { breakLine: true } },
             { text: `Fecha: ${D.FECHA}` }],
    { x: 9.6, y: 5.3, w: W - M - 9.6, h: 1.1, fontSize: 14, color: C.background1, margin: 0, valign: "top", isTextBox: true, objectName: "Docente y fecha" });
  s.addNotes(D.NOTAS[0]);
}

// ------------------------------------------------------------- 2. Importancia
{
  const s = content("Introducción", "¿Por qué el casino necesita un plan de riesgos?");
  const items = [
    ["dinero", "Proteger el dinero", "La caja y el juego mueven efectivo todo el día. Una falla o un fraude es pérdida directa."],
    ["ley", "Cumplir la ley", "El casino debe respetar su permiso, prevenir el lavado de dinero y cuidar los datos personales."],
    ["confianza", "Cuidar la confianza", "Si un cliente duda de la limpieza del juego o de sus datos, no regresa."],
  ];
  const cw = (W - 2 * M - 2 * 0.3) / 3;
  items.forEach(([ico, t, b], k) => {
    const x = M + k * (cw + 0.3), y = 1.55;
    card(s, x, y, cw, 3.55, `Tarjeta ${t}`);
    iconCircle(s, x + 0.35, y + 0.35, 0.95, ico, `Ícono ${t}`);
    s.addText(t, { x: x + 0.35, y: y + 1.5, w: cw - 0.7, h: 0.55, fontSize: 22, bold: true, color: C.text2, margin: 0,
      fontFace: THEME.headFontFace, isTextBox: true, objectName: `Título ${t}` });
    s.addText(b, { x: x + 0.35, y: y + 2.1, w: cw - 0.7, h: 1.25, fontSize: 16, color: C.text1, margin: 0, valign: "top",
      isTextBox: true, objectName: `Texto ${t}` });
  });
  card(s, M, 5.45, W - 2 * M, 1.1, "Mensaje clave", C.text2);
  s.addText([
    { text: "El plan responde tres preguntas: ", options: { bold: true, color: C.accent1 } },
    { text: "¿qué puede salir mal?, ¿qué tan grave sería? y ¿qué hacemos antes de que pase?", options: { color: C.background1 } },
  ], { x: M + 0.35, y: 5.45, w: W - 2 * M - 0.7, h: 1.1, fontSize: 19, valign: "middle", margin: 0, isTextBox: true, objectName: "Mensaje clave texto" });
  s.addNotes(D.NOTAS[1]);
}

// ------------------------------------------------------------- 3. Cómo medimos
{
  const s = content("Introducción", "¿Cómo medimos cada riesgo?");
  const boxes = [
    ["Probabilidad", "¿Qué tan seguido puede pasar?", "Alta · Media · Baja"],
    ["Impacto", "¿Cuánto daño haría?", "Alto · Medio · Bajo"],
    ["Nivel de riesgo", "Qué tan urgente es atenderlo", "Crítico · Alto · Moderado · Bajo"],
  ];
  const bw = 3.45, gap = 0.8, y = 1.6, bh = 2.0;
  boxes.forEach(([t, q, sc], k) => {
    const x = M + k * (bw + gap);
    card(s, x, y, bw, bh, `Caja ${t}`, k === 2 ? C.text2 : C.background2);
    const tc = k === 2 ? C.background1 : C.text2;
    s.addText(t, { x: x + 0.3, y: y + 0.25, w: bw - 0.6, h: 0.5, fontSize: 22, bold: true, color: k === 2 ? C.accent1 : tc,
      fontFace: THEME.headFontFace, margin: 0, isTextBox: true, objectName: `Título ${t}` });
    s.addText(q, { x: x + 0.3, y: y + 0.8, w: bw - 0.6, h: 0.5, fontSize: 16, color: k === 2 ? C.background1 : C.text1,
      margin: 0, isTextBox: true, objectName: `Pregunta ${t}` });
    s.addText(sc, { x: x + 0.3, y: y + 1.35, w: bw - 0.6, h: 0.45, fontSize: 14, bold: true, color: k === 2 ? "CDD5E3" : C.accent6,
      margin: 0, isTextBox: true, objectName: `Escala ${t}` });
    if (k < 2) {
      s.addText(k === 0 ? "+" : "=", { x: x + bw, y, w: gap, h: bh, fontSize: 40, bold: true, align: "center", valign: "middle",
        color: C.accent1, margin: 0, isTextBox: true, objectName: `Operador ${k}` });
    }
  });
  const lv = [
    ["Crítico", "Actuar ya", "Revisión semanal"],
    ["Alto", "Plan en 30 a 120 días", "Revisión quincenal"],
    ["Moderado", "Controles razonables", "Revisión mensual"],
    ["Bajo", "Aceptar y vigilar", "Revisión trimestral"],
  ];
  const lw = (W - 2 * M - 3 * 0.3) / 4;
  lv.forEach(([n, a, f], k) => {
    const x = M + k * (lw + 0.3);
    levelChip(s, x, 4.0, lw, 0.55, n, n, `Nivel ${n}`, 16);
    s.addText([{ text: a, options: { bold: true, breakLine: true } }, { text: f, options: { color: C.accent6 } }],
      { x, y: 4.65, w: lw, h: 0.8, fontSize: 15, color: C.text1, align: "center", margin: 0, valign: "top", isTextBox: true,
        objectName: `Qué hacer ${n}` });
  });
  s.addText([
    { text: "Cuatro formas de responder:  ", options: { bold: true, color: C.text2 } },
    { text: "Evitar", options: { bold: true, color: C.accent1 } }, { text: " (quitar la causa) · " },
    { text: "Mitigar", options: { bold: true, color: C.accent1 } }, { text: " (reducirlo) · " },
    { text: "Transferir", options: { bold: true, color: C.accent1 } }, { text: " (contrato o seguro) · " },
    { text: "Aceptar", options: { bold: true, color: C.accent1 } }, { text: " (vigilarlo)" },
  ], { x: M, y: 5.85, w: W - 2 * M, h: 0.6, fontSize: 16, color: C.text1, margin: 0, valign: "middle", isTextBox: true,
       objectName: "Estrategias" });
  s.addNotes(D.NOTAS[2]);
}

// ------------------------------------------------------------- 4. Fases ISO 31000
pres.addSection({ title: "Implementación de ISO 31000" });
{
  const s = content("Implementación de ISO 31000", "Implementamos ISO 31000 en 6 fases");
  s.addText("ISO 31000 es una guía internacional para gestionar riesgos. No se certifica: nos da un método común para que todas las áreas midan y atiendan los riesgos igual.",
    { x: M, y: 1.3, w: W - 2 * M, h: 0.75, fontSize: 17, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: "Qué es ISO 31000" });
  const months = ["May", "May–Jun", "Jun", "Jun–Ago", "Ago–Sep", "Sep–Oct"];
  const x0 = M + 0.9, x1 = W - M - 0.9, ly = 3.05;
  s.addShape(pres.shapes.LINE, { x: x0, y: ly, w: x1 - x0, h: 0, line: { color: C.accent6, width: 2 }, objectName: "Línea del tiempo" });
  const step = (x1 - x0) / 5;
  D.FASES.forEach((f, k) => {
    const cx = x0 + k * step, d = 0.7;
    s.addText(months[k], { x: cx - 1, y: 2.2, w: 2, h: 0.4, fontSize: 14, bold: true, color: C.accent1, align: "center",
      margin: 0, isTextBox: true, objectName: `Mes fase ${f.n}` });
    badge(s, cx - d / 2, ly - d / 2, d, String(f.n), `Fase ${f.n}`, C.text2, C.accent1, 22);
    s.addText([{ text: f.nombre, options: { bold: true, breakLine: true } },
               { text: `Semanas ${f.ini}–${f.fin}`, options: { color: C.accent6, fontSize: 13 } }],
      { x: cx - 1.0, y: 3.55, w: 2.0, h: 1.2, fontSize: 15, color: C.text2, align: "center", valign: "top", margin: 0,
        isTextBox: true, objectName: `Nombre fase ${f.n}` });
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: M, y: 4.9, w: W - 2 * M, h: 0.55, rectRadius: 0.1, fill: { color: C.accent1 },
    line: { color: C.accent1 }, objectName: "Banda comunicación" });
  s.addText("Durante las 24 semanas: comunicación y consulta con todas las áreas", { x: M, y: 4.9, w: W - 2 * M, h: 0.55,
    fontSize: 16, bold: true, color: C.text2, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Banda comunicación texto" });
  const stats = [["24", "semanas, de mayo a octubre de 2026"], ["6", "fases y un Comité de Riesgos"], ["1", "revisión completa al año (noviembre)"]];
  const sw = (W - 2 * M - 2 * 0.3) / 3;
  stats.forEach(([n, l], k) => {
    const x = M + k * (sw + 0.3);
    card(s, x, 5.7, sw, 0.95, `Dato ${k}`);
    s.addText(n, { x: x + 0.25, y: 5.7, w: 0.9, h: 0.95, fontSize: 32, bold: true, color: C.text2, valign: "middle", margin: 0,
      fontFace: THEME.headFontFace, isTextBox: true, objectName: `Dato ${k} número` });
    s.addText(l, { x: x + 1.15, y: 5.7, w: sw - 1.35, h: 0.95, fontSize: 15, color: C.text1, valign: "middle", margin: 0,
      isTextBox: true, objectName: `Dato ${k} texto` });
  });
  s.addNotes(D.NOTAS[3]);
}

// ------------------------------------------------------------- 5. Qué y quién por fase
{
  const s = content("Implementación de ISO 31000", "Qué hicimos en cada fase y quién la encabezó");
  const short = {
    1: ["La dirección aprueba la política de riesgos y crea el Comité de Riesgos.", "Dirección General"],
    2: ["Definimos roles, escalas de medición y la plantilla de la matriz.", "Gerente de Riesgos y Cumplimiento"],
    3: ["Inventario de sistemas y procesos, análisis FODA y leyes aplicables.", "Director de TI y Oficial de Cumplimiento PLD"],
    4: ["Encuestas, entrevistas y lluvia de ideas: 12 riesgos calificados.", "Equipo de riesgos con los dueños de cada riesgo"],
    5: ["Una estrategia y un plan por riesgo; el Comité aprueba presupuesto.", "Dueños de riesgo y Comité de Riesgos"],
    6: ["Arranca el tablero de indicadores y el primer informe al Comité.", "Gerente de Riesgos y Cumplimiento"],
  };
  const cw = (W - 2 * M - 2 * 0.3) / 3, ch = 2.45;
  D.FASES.forEach((f, k) => {
    const x = M + (k % 3) * (cw + 0.3), y = 1.45 + Math.floor(k / 3) * (ch + 0.3);
    card(s, x, y, cw, ch, `Tarjeta fase ${f.n}`);
    badge(s, x + 0.25, y + 0.25, 0.6, String(f.n), `Número fase ${f.n}`, C.text2, C.accent1, 18);
    s.addText(f.nombre, { x: x + 1.0, y: y + 0.25, w: cw - 1.2, h: 0.6, fontSize: 18, bold: true, color: C.text2, valign: "middle",
      margin: 0, fontFace: THEME.headFontFace, isTextBox: true, objectName: `Título fase ${f.n}` });
    s.addText(short[f.n][0], { x: x + 0.25, y: y + 1.0, w: cw - 0.5, h: 0.85, fontSize: 15, color: C.text1, valign: "top",
      margin: 0, isTextBox: true, objectName: `Qué fase ${f.n}` });
    s.addText([{ text: "Encabezó: ", options: { bold: true, color: C.accent1 } }, { text: short[f.n][1] }],
      { x: x + 0.25, y: y + 1.85, w: cw - 0.5, h: 0.45, fontSize: 13, color: C.accent6, valign: "top", margin: 0,
        isTextBox: true, objectName: `Quién fase ${f.n}` });
  });
  s.addNotes(D.NOTAS[4]);
}

// ------------------------------------------------------------- 6. Problemas
{
  const s = content("Implementación de ISO 31000", "Problemas que encontramos y cómo los resolvimos");
  const rows = [
    ["El personal sentía que era una auditoría para buscar culpables", "Encuestas anónimas y explicar que el objetivo es prevenir"],
    ["Turnos rotativos: no se podía reunir a todos", "Sesiones de 30 minutos en cada turno y encuesta en línea"],
    ["No existía un registro de incidentes pasados", "Reconstruimos la historia y creamos una bitácora única"],
    ["El presupuesto no alcanzaba para todo", "El mapa de calor nos dijo qué atender primero"],
  ];
  const lx = M, lw = 5.4, ax = M + 5.55, rx = M + 6.35, rw = W - M - rx, rh = 1.0, g = 0.22;
  s.addText("Problema", { x: lx, y: 1.35, w: lw, h: 0.4, fontSize: 15, bold: true, color: C.accent6, margin: 0, isTextBox: true, objectName: "Encabezado problema" });
  s.addText("Solución", { x: rx, y: 1.35, w: rw, h: 0.4, fontSize: 15, bold: true, color: C.accent6, margin: 0, isTextBox: true, objectName: "Encabezado solución" });
  rows.forEach(([p, sol], k) => {
    const y = 1.85 + k * (rh + g);
    card(s, lx, y, lw, rh, `Problema ${k + 1}`);
    s.addText(p, { x: lx + 0.3, y, w: lw - 0.5, h: rh, fontSize: 16, color: C.text1, valign: "middle", margin: 0, isTextBox: true, objectName: `Problema ${k + 1} texto` });
    s.addShape(pres.shapes.RIGHT_ARROW, { x: ax, y: y + rh / 2 - 0.2, w: 0.6, h: 0.4, fill: { color: C.accent1 }, line: { color: C.accent1 }, objectName: `Flecha ${k + 1}` });
    card(s, rx, y, rw, rh, `Solución ${k + 1}`, C.text2);
    s.addText(sol, { x: rx + 0.3, y, w: rw - 0.5, h: rh, fontSize: 16, bold: true, color: C.background1, valign: "middle", margin: 0, isTextBox: true, objectName: `Solución ${k + 1} texto` });
  });
  s.addText("Otros retos: áreas con listas de riesgos separadas, cámaras y tragamonedas antiguas, y una matriz previa con otra escala.",
    { x: M, y: 6.45, w: W - 2 * M, h: 0.4, fontSize: 13, italic: true, color: C.accent6, margin: 0, isTextBox: true, objectName: "Otros retos" });
  s.addNotes(D.NOTAS[5]);
}

// ------------------------------------------------------------- 7. Impacto en objetivos
pres.addSection({ title: "Riesgos y tratamiento" });
{
  const s = content("Riesgos y tratamiento", "Cómo afectan los riesgos a los objetivos del negocio");
  const objs = [
    ["engrane", "Operar sin interrupciones", "Sin sistemas no hay caja, pagos ni tragamonedas.", ["R7", "R8", "R11", "R12"]],
    ["check", "Juego justo y confiable", "Un fraude en mesas o máquinas causa pérdidas y disputas.", ["R1", "R2", "R3", "R5"]],
    ["ley", "Cumplir la ley", "El lavado de dinero o una fuga de datos traen multas.", ["R6", "R10"]],
    ["confianza", "Clientes que regresan", "Datos expuestos o saldos alterados alejan a los clientes.", ["R4", "R9", "R10"]],
  ];
  const cw = (W - 2 * M - 0.3) / 2, ch = 2.45;
  objs.forEach(([ico, t, b, ids], k) => {
    const x = M + (k % 2) * (cw + 0.3), y = 1.45 + Math.floor(k / 2) * (ch + 0.3);
    card(s, x, y, cw, ch, `Objetivo ${t}`);
    iconCircle(s, x + 0.3, y + 0.3, 0.8, ico, `Ícono ${t}`);
    s.addText(t, { x: x + 1.3, y: y + 0.3, w: cw - 1.6, h: 0.8, fontSize: 21, bold: true, color: C.text2, valign: "middle",
      margin: 0, fontFace: THEME.headFontFace, isTextBox: true, objectName: `Título ${t}` });
    s.addText(b, { x: x + 0.3, y: y + 1.2, w: cw - 0.6, h: 0.5, fontSize: 16, color: C.text1, margin: 0, valign: "top",
      isTextBox: true, objectName: `Texto ${t}` });
    ids.forEach((id, j) => {
      levelChip(s, x + 0.3 + j * 1.05, y + 1.8, 0.9, 0.42, R[id].nivel, id, `Chip ${t} ${id}`, 14);
    });
  });
  s.addNotes(D.NOTAS[6]);
}

// ------------------------------------------------------------- 8. Mapa de calor
{
  const s = content("Riesgos y tratamiento", "Mapa de calor: dónde están nuestros 12 riesgos");
  const ar = 992 / 692;
  const h = 5.35, w = h * ar;
  s.addImage({ path: img("mapa_calor.png"), x: M, y: 1.35, w, h, objectName: "Mapa de calor",
    altText: "Mapa de calor 3x3 de probabilidad contra impacto con los riesgos R1 a R12" });
  const cnt = Object.fromEntries(D.NIVELES.map((n) => [n, D.RIESGOS.filter((r) => r.nivel === n)]));
  const px = M + w + 0.45, pw = W - M - px;
  D.NIVELES.forEach((n, k) => {
    const y = 1.5 + k * 1.0;
    levelChip(s, px, y + 0.1, 1.5, 0.6, n, n, `Conteo ${n} etiqueta`, 15);
    s.addText([{ text: String(cnt[n].length), options: { bold: true, fontSize: 28, color: C.text2 } },
               { text: "  " + cnt[n].map((r) => r.id).join(", "), options: { fontSize: 14, color: C.accent6 } }],
      { x: px + 1.65, y, w: pw - 1.65, h: 0.8, valign: "middle", margin: 0, isTextBox: true, objectName: `Conteo ${n}` });
  });
  card(s, px, 5.6, pw, 1.05, "Meta", C.text2);
  s.addText([{ text: "Meta a 12 meses: ", options: { bold: true, color: C.accent1 } },
             { text: "bajar de 6 a 3 los riesgos Crítico o Alto.", options: { color: C.background1 } }],
    { x: px + 0.25, y: 5.6, w: pw - 0.5, h: 1.05, fontSize: 15, valign: "middle", margin: 0, isTextBox: true, objectName: "Meta texto" });
  s.addNotes(D.NOTAS[7]);
}

// ------------------------------------------------------------- 9 y 10. Tratamiento
function tablaRiesgos(s, ids) {
  const hdr = ["ID", "Riesgo", "Nivel", "Estrategia", "Qué haremos", "Responsable"].map((t) => ({
    text: t, options: { bold: true, color: C.background1, fill: { color: C.text2 }, fontSize: 14, valign: "middle" } }));
  const rows = [hdr];
  ids.forEach((id, k) => {
    const r = R[id];
    const base = { fontSize: 14, color: C.text1, valign: "middle", fill: { color: k % 2 ? C.background2 : C.background1 } };
    rows.push([
      { text: id, options: { ...base, bold: true, color: C.text2, align: "center" } },
      { text: r.corto, options: { ...base } },
      { text: r.nivel, options: { ...base, bold: true, align: "center", color: LVL_TXT[r.nivel], fill: { color: LVL[r.nivel] } } },
      { text: r.estrategia, options: { ...base, bold: true, align: "center" } },
      { text: r.clave, options: { ...base } },
      { text: r.responsable, options: { ...base, fontSize: 13 } },
    ]);
  });
  s.addTable(rows, { x: M, y: 1.4, w: W - 2 * M, colW: [0.7, 3.0, 1.35, 1.5, 3.6, 1.983], rowH: 0.7,
    border: { type: "solid", pt: 0.75, color: "D7DCE3" }, margin: [0.04, 0.1, 0.04, 0.1], objectName: "Tabla de riesgos" });
}
{
  const s = content("Riesgos y tratamiento", "Riesgos prioritarios y cómo los vamos a tratar");
  const ids = D.RIESGOS.filter((r) => r.nivel === "Crítico").concat(D.RIESGOS.filter((r) => r.nivel === "Alto")).map((r) => r.id);
  tablaRiesgos(s, ids);
  s.addNotes(D.NOTAS[8]);
}
{
  const s = content("Riesgos y tratamiento", "Riesgos moderados y bajos: control y vigilancia");
  const ids = D.RIESGOS.filter((r) => r.nivel === "Moderado").concat(D.RIESGOS.filter((r) => r.nivel === "Bajo")).map((r) => r.id);
  tablaRiesgos(s, ids);
  s.addNotes(D.NOTAS[9]);
}

// ------------------------------------------------------------- 11. Seguimiento
pres.addSection({ title: "Seguimiento y cierre" });
{
  const s = content("Seguimiento y cierre", "¿Cómo sabremos si el plan funciona?");
  const k7 = D.KPI_KRI.R7;
  const cw = (W - 2 * M - 0.3) / 2;
  const items = [
    ["KPI", "¿El control se está aplicando?", `Ejemplo (R7): ${k7.kpi}. Meta: ${k7.meta}.`],
    ["KRI", "¿Qué tan expuestos estamos?", `Ejemplo (R7): ${k7.kri}. Alerta si es ${k7.umbral}.`],
  ];
  items.forEach(([t, q, ex], k) => {
    const x = M + k * (cw + 0.3), y = 1.45;
    card(s, x, y, cw, 2.55, `Tarjeta ${t}`);
    badge(s, x + 0.3, y + 0.3, 0.95, t, `Insignia ${t}`, C.text2, C.accent1, 18);
    s.addText(q, { x: x + 1.45, y: y + 0.3, w: cw - 1.75, h: 0.95, fontSize: 21, bold: true, color: C.text2, valign: "middle",
      margin: 0, fontFace: THEME.headFontFace, isTextBox: true, objectName: `Pregunta ${t}` });
    s.addText(ex, { x: x + 0.3, y: y + 1.45, w: cw - 0.6, h: 0.9, fontSize: 15, color: C.text1, valign: "top", margin: 0,
      isTextBox: true, objectName: `Ejemplo ${t}` });
  });
  s.addText("Cada cuándo revisamos", { x: M, y: 4.3, w: 6, h: 0.45, fontSize: 18, bold: true, color: C.text2, margin: 0,
    fontFace: THEME.headFontFace, isTextBox: true, objectName: "Título frecuencia" });
  const lw = (W - 2 * M - 3 * 0.3) / 4;
  D.NIVELES.forEach((n, k) => {
    const x = M + k * (lw + 0.3);
    levelChip(s, x, 4.85, lw, 0.55, n, `${n}: ${D.FRECUENCIA_MONITOREO[n].toLowerCase()}`, `Frecuencia ${n}`, 15);
  });
  s.addText([
    { text: "Reporte mensual ", options: { bold: true, color: C.text2 } }, { text: "al Comité de Riesgos con el mapa de calor y los indicadores.  " },
    { text: "Informe trimestral ", options: { bold: true, color: C.text2 } }, { text: "a la Dirección General." },
  ], { x: M, y: 5.7, w: W - 2 * M, h: 0.8, fontSize: 16, color: C.text1, margin: 0, valign: "top", isTextBox: true, objectName: "Reportes" });
  s.addNotes(D.NOTAS[10]);
}

// ------------------------------------------------------------- 12. Conclusión
{
  const s = pres.addSlide({ masterName: "CIERRE", sectionTitle: "Seguimiento y cierre" });
  s.addText("Conclusión y próximos pasos", { placeholder: "title" });
  const msgs = [
    ["Mejora continua", "Los riesgos cambian. Medimos, revisamos y ajustamos cada trimestre, y el plan completo cada año."],
    ["Cultura de riesgos", "Cada empleado es parte del control: el cajero que rota, el crupier que revisa la baraja y quien reporta un correo sospechoso."],
  ];
  msgs.forEach(([t, b], k) => {
    const y = 1.5 + k * 2.1;
    s.addText(t, { x: M, y, w: 5.9, h: 0.55, fontSize: 24, bold: true, color: C.accent1, margin: 0, fontFace: THEME.headFontFace,
      isTextBox: true, objectName: `Mensaje ${k + 1} título` });
    s.addText(b, { x: M, y: y + 0.6, w: 5.9, h: 1.2, fontSize: 17, color: C.background1, margin: 0, valign: "top",
      isTextBox: true, objectName: `Mensaje ${k + 1} texto` });
  });
  const steps = [
    ["30 días", "Doble factor y antivirus avanzado, rotación de cajeros, alertas de cámaras, bloqueo de USB"],
    ["90 días", "Red segmentada, datos cifrados, expedientes de clientes y alertas antilavado"],
    ["120 días", "Control de cuentas de administrador, prevención de fugas y sensores en tragamonedas"],
  ];
  const px = 7.1, pw = W - M - px;
  steps.forEach(([t, b], k) => {
    const y = 1.5 + k * 1.45;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px, y, w: pw, h: 1.25, rectRadius: 0.1, fill: { color: "1B2F52" },
      line: { color: "1B2F52" }, objectName: `Paso ${k + 1}` });
    s.addText(t, { x: px + 0.25, y, w: 1.35, h: 1.25, fontSize: 19, bold: true, color: C.accent1, valign: "middle", margin: 0,
      isTextBox: true, objectName: `Paso ${k + 1} plazo` });
    s.addText(b, { x: px + 1.65, y, w: pw - 1.85, h: 1.25, fontSize: 15, color: C.background1, valign: "middle", margin: 0,
      isTextBox: true, objectName: `Paso ${k + 1} texto` });
  });
  s.addText("Gracias. ¿Preguntas?", { x: M, y: 5.95, w: W - 2 * M, h: 0.7, fontSize: 28, bold: true, color: C.background1,
    margin: 0, fontFace: THEME.headFontFace, isTextBox: true, objectName: "Cierre" });
  s.addNotes(D.NOTAS[11]);
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  const { applyTheme } = require(path.join(SKILL, "scripts", "apply_theme.js"));
  await applyTheme(OUT, THEME);
  console.log("PPTX:", OUT);
})().catch((e) => { console.error(e); process.exit(1); });
