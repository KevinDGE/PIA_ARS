// Renderizado con Chromium (Playwright):
//   node render.js png <archivo.svg> <salida.png> [escala]
//   node render.js pdf <archivo.html> <salida.pdf>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const [mode, input, output, scaleArg] = process.argv.slice(2);
  const browser = await chromium.launch();
  try {
    if (mode === 'png' || mode === 'pngt') {
      const svg = fs.readFileSync(input, 'utf8');
      const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
      const w = Math.ceil(+m[1]), h = Math.ceil(+m[2]);
      const scale = +(scaleArg || 3);
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
      await page.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
      await page.evaluate(() => document.fonts.ready);
      await page.locator('svg').screenshot({ path: output, omitBackground: mode === 'pngt' });
    } else if (mode === 'pdf') {
      const page = await browser.newPage();
      await page.goto('file://' + path.resolve(input));
      await page.evaluate(() => document.fonts.ready);
      await page.pdf({ path: output, format: 'Letter', printBackground: true, preferCSSPageSize: true,
                       outline: true, tagged: true });
    } else {
      throw new Error('modo desconocido: ' + mode);
    }
  } finally {
    await browser.close();
  }
})().catch(e => { console.error(e); process.exit(1); });
