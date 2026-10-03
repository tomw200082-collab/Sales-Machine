const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 11000, height: 13800 }, deviceScaleFactor: 0.35 });
  await p.goto('file://' + __dirname + '/out/preview.html');
  await p.waitForTimeout(500);
  const res = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll('[data-chk]').forEach(e => {
      const kind = e.dataset.chk;
      if (kind === 'rect') { if (e.scrollHeight > e.clientHeight + 2 || e.scrollWidth > e.clientWidth + 2) out.push(['rect overflow', e.textContent.slice(0,40), e.clientWidth, e.clientHeight, e.scrollWidth, e.scrollHeight]); }
      else { const mh = +e.dataset.maxh; if (mh && e.offsetHeight > mh + 2) out.push(['text too tall', e.textContent.slice(0,40), e.offsetHeight, mh]); }
    });
    return out;
  });
  console.log(JSON.stringify(res, null, 0));
  const ids = await p.evaluate(() => [...document.querySelectorAll('.fr')].map(f => f.id));
  for (const id of ids) { await p.locator('#' + id).screenshot({ path: `out/shot_${id}.png` }); }
  await b.close();
})();
