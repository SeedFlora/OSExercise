// Capture a real browser view of the retained Linux PTY transcript.
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const base = path.resolve(__dirname, '..');
const names = ['00_lingkungan', '01_loket_label', '02_dua_petugas', '03_ganti_program', '04_gagal_ganti'];
const titles = ['Lingkungan Linux + terminal PTY', 'Loket label', 'Dua petugas', 'Pergantian program berhasil', 'Pergantian program gagal'];
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const cards = names.map((n,i) => {
  const output = fs.readFileSync(path.join(base,'logs',n+'.txt'),'utf8').trimEnd();
  return `<article id="${n}"><header><span class="dot"></span><span class="dot"></span><span class="dot"></span><b>${titles[i]}</b></header><div class="tag">LINUX / PTY &nbsp; | &nbsp; TRANSKRIP EKSEKUSI AKTUAL</div><pre>${esc(output)}</pre><footer>${n}.pty.log &nbsp; | &nbsp; 13 Oktober 2026</footer></article>`;
}).join('\n');
const html = `<!doctype html><html lang="id"><meta charset="utf-8"><title>Bukti eksekusi konsep proses Linux</title><style>
*{box-sizing:border-box}body{margin:0;padding:24px;background:#e8eff3;font-family:Arial,sans-serif}article{width:720px;background:#102b3b;color:#eaf6fc;border-radius:12px;overflow:hidden;margin:0 0 24px}header{display:flex;align-items:center;gap:7px;padding:17px 22px;background:#18394c;font-size:17px}header b{margin-left:12px}.dot{height:9px;width:9px;border-radius:50%;background:#58a9bc}.dot:first-child{background:#f09886}.dot:nth-child(2){background:#efd07c}.tag{font-size:12px;color:#80c8d5;letter-spacing:1.2px;padding:17px 23px 5px}pre{font-family:Consolas,'Courier New',monospace;font-size:19px;line-height:1.42;white-space:pre-wrap;overflow-wrap:anywhere;margin:10px 23px 19px}footer{font-family:Consolas,monospace;font-size:12px;color:#91adbb;border-top:1px solid #2c4c5e;padding:13px 23px}
</style><body>${cards}</body></html>`;
const htmlPath=path.join(base,'logs','tampilan_hasil.html');
fs.writeFileSync(htmlPath,html,'utf8');
(async()=>{
  const browser=await chromium.launch({headless:true,...(process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH ? {executablePath:process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH} : {})});
  const page=await browser.newPage({viewport:{width:790,height:900},deviceScaleFactor:2});
  await page.goto(pathToFileURL(htmlPath).href);
  await page.evaluate(()=>document.fonts.ready);
  const result=[];
  for(const n of names){
    const el=page.locator('[id="'+n+'"]');
    await el.screenshot({path:path.join(base,'screenshots',n+'.png')});
    result.push({name:n,bounds:await el.boundingBox()});
  }
  fs.writeFileSync(path.join(base,'screenshots','capture_metadata.json'),JSON.stringify({kind:'Browser screenshot of actual, unmodified normalized Linux PTY output',sourceHtml:'logs/tampilan_hasil.html',shots:result},null,2));
  await browser.close();
  console.log('Five real transcript views captured.');
})().catch(e=>{console.error(e);process.exit(1)});
