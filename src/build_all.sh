#!/usr/bin/env bash
# Genera los tres entregables desde data.py. Uso: bash src/build_all.sh
set -euo pipefail
cd "$(dirname "$0")"
SKILLS=${SKILLS:-/root/.claude/skills/synced/a4e11c3f-8587-4905-836a-cf55136f08ee_2901baed-2857-4f83-b1de-faa0b9d41784}
export PPTX_SKILL="$SKILLS/pptx"
export NODE_PATH="$PWD/node_modules:$(npm root -g):/opt/node-tools/node_modules"
[ -d node_modules/pptxgenjs ] || npm install --no-audit --no-fund
python3 export_assets.py            # JSON + PNG (mapa de calor, línea del tiempo, íconos)
python3 build_doc.py                # PDF
python3 build_xlsx.py               # Excel
python3 "$SKILLS/xlsx/scripts/recalc.py" ../entregables/Matriz_de_Riesgos_Casino_Royale.xlsx 90
node build_pptx.js                  # PowerPoint
python3 "$PPTX_SKILL/scripts/office/validate.py" ../entregables/Presentacion_Ejecutiva_Casino_Royale.pptx
python3 verify.py                   # coherencia entre los tres entregables
