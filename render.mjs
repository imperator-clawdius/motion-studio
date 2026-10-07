import puppeteer from 'puppeteer-core';
import { mkdirSync } from 'node:fs';

const FPS = 30, DUR = 15, W = 1920, H = 1080;
const frames = FPS * DUR;

mkdirSync('./frames', { recursive: true });

const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome',
  headless: true,
  args: ['--no-sandbox', '--disable-setuid-sandbox', '--force-device-scale-factor=1', '--hide-scrollbars'],
});

const page = await browser.newPage();
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
await page.goto('file://' + process.cwd() + '/index.html', { waitUntil: 'load', timeout: 30000 });
// wait for fonts to settle (best-effort; falls back to system sans if offline)
await page.evaluate(() => document.fonts.ready).catch(() => {});

const t0 = Date.now();
for (let i = 0; i < frames; i++) {
  const t = i / FPS;
  await page.evaluate((tt) => window.seek(tt), t);
  await page.screenshot({ path: `./frames/f${String(i).padStart(4, '0')}.png` });
  if (i % 45 === 0) console.log(`frame ${i}/${frames}`);
}
await browser.close();
console.log(`done ${frames} frames in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
