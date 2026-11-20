# PIA_ARS · Administración de Riesgos de TI (grupo 061, UANL)

Plan de administración de riesgos de TI para **Casino Royale Enterprises** (caso académico ficticio), basado en ISO 31000:2018.

## Entregables (`entregables/`)

| Archivo | Contenido |
|---|---|
| `PIA_061_Casino_Royale_Administracion_de_Riesgos_TI.pdf` | Documento completo (portada, índice, secciones 1 a 8 y referencias APA 7) |
| `Matriz_de_Riesgos_Casino_Royale.xlsx` | Hojas «Matriz de riesgos», «KPI y KRI» y «Mapa de calor» con filtros, encabezados fijos, colores por nivel y formato de impresión |
| `Presentacion_Ejecutiva_Casino_Royale.pptx` | 12 diapositivas para público no técnico, con notas del orador |
| `Guion_Presentacion_Ejecutiva.pdf` | Guion dividido por integrante (David abre con la introducción), con miniatura de cada diapositiva, tiempos y preguntas probables |

## Material de apoyo (`apoyo/`)

`Guia_de_defensa_del_plan.pdf`: para preparar la exposición. Explica por qué se eligió cada parte del plan, qué mejoras y alternativas tiene a futuro y sus posibles puntos de falla. No es un entregable del PIA.

## Cómo regenerarlos

Todos los datos (riesgos, niveles, estrategias, responsables, KPI/KRI, fases) viven en `src/data.py`, y el guion de la presentación en `src/guion.py` (de ahí salen también las notas del orador). Para que los tres entregables sigan coincidiendo, cambia los datos solo ahí y ejecuta:

```bash
bash src/build_all.sh
```

El script genera el PDF (HTML + Chromium), el Excel (openpyxl, con fórmulas recalculadas), el PowerPoint (pptxgenjs) y al final corre `src/verify.py`, que compara IDs, niveles, estrategias y responsables entre los tres archivos y revisa el índice del PDF.
