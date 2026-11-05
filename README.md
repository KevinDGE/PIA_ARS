# PIA_ARS · Administración de Riesgos de TI (grupo 061, UANL)

Plan de administración de riesgos de TI para **Casino Royale Enterprises** (caso académico ficticio), basado en ISO 31000:2018.

## Entregables (`entregables/`)

| Archivo | Contenido |
|---|---|
| `PIA_061_Casino_Royale_Administracion_de_Riesgos_TI.pdf` | Documento completo (portada, índice, secciones 1 a 8 y referencias APA 7) |
| `Matriz_de_Riesgos_Casino_Royale.xlsx` | Hojas «Matriz de riesgos», «KPI y KRI» y «Mapa de calor» con filtros, encabezados fijos, colores por nivel y formato de impresión |
| `Presentacion_Ejecutiva_Casino_Royale.pptx` | 12 diapositivas para público no técnico, con notas del orador |

## Cómo regenerarlos

Todos los datos (riesgos, niveles, estrategias, responsables, KPI/KRI, fases) viven en `src/data.py`. Para que los tres entregables sigan coincidiendo, cambia los datos solo ahí y ejecuta:

```bash
bash src/build_all.sh
```

El script genera el PDF (HTML + Chromium), el Excel (openpyxl, con fórmulas recalculadas), el PowerPoint (pptxgenjs) y al final corre `src/verify.py`, que compara IDs, niveles, estrategias y responsables entre los tres archivos y revisa el índice del PDF.

## Pendientes

- Matrículas de David Emiliano Rangel Tovar, Fernando Garza Chavez, Alejandro Martinez Moya y Rene Villareal Torres (`INTEGRANTES` en `src/data.py`).
- Nombre de la facultad (`FACULTAD` en `src/data.py`).
- Logos de la UANL y de la facultad (ver `assets/logos/LEEME.md`).
