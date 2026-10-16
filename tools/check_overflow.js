// Marp の HTML 出力を headless Chromium で開き、スライドからはみ出した要素を報告する。
//
//   make html && node tools/check_overflow.js [out/lambda.html]
//
// - 各 <section> の内側（padding を除いた領域）より下・右に出た要素を数える。
//   KaTeX の MathML（非表示）と SVG の path は誤検出になるので除く。
// - <pre> の横・縦のスクロール（コードの切れ）も検出する。
// - はみ出しがあれば終了コード 1。
//
// puppeteer-core は marp-cli が npx キャッシュに入れたものを使う（make html を一度実行しておく）。
// 見つからないときは PUPPETEER_CORE=/path/to/node_modules/puppeteer-core を指定する。
// ブラウザは CHROME_PATH、なければ一般的な場所から探す。
// snap 版 Chromium は /tmp などを file:// で読めないため、内蔵の HTTP サーバー経由で開く。

const fs = require("fs");
const http = require("http");
const os = require("os");
const path = require("path");

function findPuppeteer() {
  if (process.env.PUPPETEER_CORE) return process.env.PUPPETEER_CORE;
  const npx = path.join(os.homedir(), ".npm", "_npx");
  for (const dir of fs.existsSync(npx) ? fs.readdirSync(npx) : []) {
    const p = path.join(npx, dir, "node_modules", "puppeteer-core");
    if (fs.existsSync(p)) return p;
  }
  throw new Error("puppeteer-core not found; run `make html` once or set PUPPETEER_CORE");
}

function findChrome() {
  const candidates = [process.env.CHROME_PATH, "/usr/bin/chromium-browser",
    "/usr/bin/chromium", "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"];
  const found = candidates.find((c) => c && fs.existsSync(c));
  if (!found) throw new Error("Chrome/Chromium not found; set CHROME_PATH");
  return found;
}

(async () => {
  const file = path.resolve(process.argv[2] || "out/lambda.html");
  const server = http.createServer((req, res) => {
    res.setHeader("Content-Type", "text/html; charset=utf-8");
    fs.createReadStream(file).pipe(res);
  });
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const puppeteer = require(findPuppeteer());
  const browser = await puppeteer.launch({ executablePath: findChrome(), args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 720 });
  await page.goto(`http://127.0.0.1:${server.address().port}/`, { waitUntil: "networkidle0" });
  await page.evaluate(() => document.fonts.ready);
  const bad = await page.evaluate(() => {
    const out = [];
    document.querySelectorAll("section[id]").forEach((s, i) => {
      const box = s.getBoundingClientRect();
      const cs = getComputedStyle(s);
      // Bespoke HTML scales slides; convert CSS px limits into screen px.
      const scale = box.width / s.offsetWidth;
      const limitB = (s.offsetHeight - parseFloat(cs.paddingBottom)) * scale + 1;
      const limitR = (s.offsetWidth - parseFloat(cs.paddingRight)) * scale + 1;
      let over = 0;
      s.querySelectorAll("*").forEach((e) => {
        if (e.closest(".katex-mathml") || e.tagName === "path") return;
        const r = e.getBoundingClientRect();
        if (!r.width && !r.height) return;
        if (r.bottom - box.top > limitB || r.right - box.left > limitR) over++;
      });
      const pre = [...s.querySelectorAll("pre")].filter(
        (p) => p.scrollWidth > p.clientWidth + 1 || p.scrollHeight > p.clientHeight + 1).length;
      const h = s.querySelector("h1, h2");
      if (over || pre) out.push({ slide: i + 1, over, pre, title: h ? h.textContent.trim() : "" });
    });
    return out;
  });
  await browser.close();
  server.close();
  for (const b of bad)
    console.log(`slide ${b.slide}: ${b.over} element(s) outside, ${b.pre} code block(s) clipped — ${b.title}`);
  console.log(bad.length ? `${bad.length} slide(s) overflow` : "no overflow");
  process.exit(bad.length ? 1 : 0);
})().catch((e) => { console.error(e.message); process.exit(2); });
