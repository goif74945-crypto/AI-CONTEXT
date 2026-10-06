#!/usr/bin/env node
'use strict';

const fs = require('fs');
const fsp = require('fs/promises');
const http = require('http');
const path = require('path');
const {spawn} = require('child_process');

const ROOT = process.cwd();
const DEMO_DIR = path.join(ROOT, 'demo');
const DEMO_FILE = path.join(DEMO_DIR, 'viralforge-black-cat.html');
const BASE_PORT = Number(process.env.PORT || 4173);

const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ViralForge Black Cat Clapping</title>
<style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020305;color:#fff;font-family:Arial,Helvetica,sans-serif}
body{display:grid;place-items:center;background:radial-gradient(circle at 50% 20%,#17233a 0,#080a10 42%,#020305 100%)}
.frame{position:relative;height:min(96vh,960px);aspect-ratio:9/16;overflow:hidden;border-radius:28px;background:radial-gradient(circle at 50% 46%,rgba(0,229,255,.22),transparent 40%),linear-gradient(180deg,#070a10,#020305);box-shadow:0 0 90px #00e5ff2e,0 30px 100px #000}
.grid{position:absolute;inset:0;background-image:linear-gradient(#00e5ff10 1px,transparent 1px),linear-gradient(90deg,#00e5ff10 1px,transparent 1px);background-size:38px 38px}
.code{position:absolute;inset:-8% -8% auto;opacity:.14;color:#00e5ff;font:700 13px/1.5 Consolas,monospace;white-space:pre;transform:rotate(-4deg) scale(1.18);animation:fall 3.3s linear infinite}
@keyframes fall{to{transform:translateY(160px) rotate(-4deg) scale(1.18)}}
.badge{position:absolute;z-index:8;top:4%;left:6%;padding:9px 15px;border:1px solid #00e5ff99;border-radius:999px;background:#0008;font-weight:900;font-size:14px;letter-spacing:2px;color:#72f6ff}
.title{position:absolute;z-index:8;top:10%;left:6%;right:6%;font:900 clamp(30px,5vh,62px)/.91 "Arial Black",Arial,sans-serif;letter-spacing:-2px;text-transform:uppercase;text-shadow:0 0 22px #00e5ff,0 8px 28px #000;animation:punch .7s cubic-bezier(.18,.85,.2,1.15) both}
.title span{color:#00e5ff}@keyframes punch{0%{transform:scale(1.55) rotate(-4deg);opacity:0}60%{transform:scale(.96) rotate(1deg)}100%{transform:scale(1);opacity:1}}
.cat{position:absolute;left:50%;top:54%;width:82%;transform:translate(-50%,-50%);filter:drop-shadow(0 35px 35px #000c);animation:catIn .55s .25s cubic-bezier(.2,.9,.25,1.25) both}
@keyframes catIn{from{transform:translate(-50%,-42%) scale(.6);opacity:0}to{transform:translate(-50%,-50%) scale(1);opacity:1}}
svg{width:100%;overflow:visible}#leftArm{transform-box:view-box;transform-origin:168px 455px;animation:leftClap .34s ease-in-out infinite alternate}#rightArm{transform-box:view-box;transform-origin:332px 455px;animation:rightClap .34s ease-in-out infinite alternate}
@keyframes leftClap{0%{transform:rotate(-22deg) translate(-18px,14px)}100%{transform:rotate(18deg) translate(38px,-5px)}}@keyframes rightClap{0%{transform:rotate(22deg) translate(18px,14px)}100%{transform:rotate(-18deg) translate(-38px,-5px)}}
#flash{transform-box:fill-box;transform-origin:center;animation:flash .34s ease-in-out infinite alternate}@keyframes flash{0%,52%{opacity:0;transform:scale(.3)}100%{opacity:.95;transform:scale(1.7)}}
#head{transform-box:fill-box;transform-origin:center;animation:bob .68s ease-in-out infinite alternate}@keyframes bob{to{transform:translateY(5px) rotate(1.7deg)}}
.caption{position:absolute;z-index:8;left:5%;right:5%;bottom:7%;text-align:center;font:900 clamp(20px,3.2vh,38px)/1.04 "Arial Black",Arial,sans-serif;text-transform:uppercase;text-shadow:0 4px 18px #000,0 0 14px #000}
.caption b{color:#00e5ff;display:inline-block;animation:pulse .68s ease-in-out infinite alternate}@keyframes pulse{to{transform:scale(1.08);text-shadow:0 0 18px #00e5ff}}
</style></head><body><main class="frame">
<div class="grid"></div><div class="code">const viral = true;
render(frame);
CAT.clap();
while(hype){ship();}
010101101010
AI → CODE → MOTION
const fps = 60;
render(frame);
CAT.clap();
while(hype){ship();}</div>
<div class="badge">VIRALFORGE // LIVE</div>
<div class="title">WHEN THE CODE<br><span>FINALLY RUNS</span></div>
<div class="cat"><svg viewBox="0 0 500 760" role="img" aria-label="Original animated black cat clapping">
<defs><radialGradient id="fur"><stop stop-color="#30343a"/><stop offset=".6" stop-color="#111318"/><stop offset="1" stop-color="#050607"/></radialGradient><radialGradient id="palm"><stop stop-color="#d7b69d"/><stop offset="1" stop-color="#9f7b67"/></radialGradient></defs>
<ellipse cx="250" cy="720" rx="150" ry="25" fill="#000" opacity=".65"/><ellipse cx="250" cy="505" rx="128" ry="176" fill="url(#fur)"/>
<g id="head"><path d="M145 228 L168 120 L226 184 Z" fill="#0a0b0e"/><path d="M355 228 L332 120 L274 184 Z" fill="#0a0b0e"/><ellipse cx="250" cy="257" rx="122" ry="108" fill="url(#fur)"/><ellipse cx="207" cy="241" rx="24" ry="15" fill="#91ff90"/><ellipse cx="293" cy="241" rx="24" ry="15" fill="#91ff90"/><ellipse cx="207" cy="241" rx="6" ry="14" fill="#090b0c"/><ellipse cx="293" cy="241" rx="6" ry="14" fill="#090b0c"/><path d="M242 277 Q250 285 258 277 Q250 295 242 277" fill="#c4888f"/><path d="M188 296 Q250 350 312 296 Q303 365 250 369 Q197 365 188 296Z" fill="#efe9df"/><path d="M202 315 Q250 346 298 315" fill="none" stroke="#34343a" stroke-width="5" stroke-linecap="round"/></g>
<g id="leftArm"><path d="M168 430 Q120 498 188 550" fill="none" stroke="#11141a" stroke-width="54" stroke-linecap="round"/><g transform="translate(184 548) rotate(-18)"><ellipse rx="44" ry="52" fill="url(#palm)"/><rect x="-47" y="-62" width="17" height="65" rx="9" fill="#c8a58e"/><rect x="-27" y="-72" width="17" height="70" rx="9" fill="#d2af96"/><rect x="-6" y="-75" width="17" height="72" rx="9" fill="#d8b69c"/><rect x="15" y="-66" width="17" height="64" rx="9" fill="#caa58e"/></g></g>
<g id="rightArm"><path d="M332 430 Q380 498 312 550" fill="none" stroke="#11141a" stroke-width="54" stroke-linecap="round"/><g transform="translate(316 548) rotate(18)"><ellipse rx="44" ry="52" fill="url(#palm)"/><rect x="30" y="-62" width="17" height="65" rx="9" fill="#c8a58e"/><rect x="10" y="-72" width="17" height="70" rx="9" fill="#d2af96"/><rect x="-11" y="-75" width="17" height="72" rx="9" fill="#d8b69c"/><rect x="-32" y="-66" width="17" height="64" rx="9" fill="#caa58e"/></g></g>
<circle id="flash" cx="250" cy="542" r="20" fill="#fff"/><circle cx="250" cy="542" r="48" fill="none" stroke="#00e5ff" stroke-width="4" opacity=".35"/>
</svg></div>
<div class="caption">AI AFTER ONE SUCCESSFUL BUILD<br><b>👏 CLAP. CLAP. CLAP.</b></div>
</main></body></html>`;

const sleep = ms => new Promise(r => setTimeout(r, ms));

function launchCode(args) {
  try {
    const child = spawn('code', args, {stdio:'ignore', detached:true});
    child.unref();
    return true;
  } catch {
    return false;
  }
}

function publicUrl(port) {
  const name = process.env.CODESPACE_NAME;
  const domain = process.env.GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN;
  if (name && domain) return `https://${name}-${port}.${domain}/viralforge-black-cat.html`;
  return `http://127.0.0.1:${port}/viralforge-black-cat.html`;
}

async function streamFile() {
  await fsp.mkdir(DEMO_DIR, {recursive:true});
  await fsp.writeFile(DEMO_FILE, '', 'utf8');
  launchCode(['--reuse-window', DEMO_FILE]);

  process.stdout.write('\x1b[2J\x1b[H🔥 ViralForge live-code boot\\n\\n');
  const chunks = html.match(/.{1,140}/gs) || [];
  for (const chunk of chunks) {
    await fsp.appendFile(DEMO_FILE, chunk, 'utf8');
    process.stdout.write('\x1b[36m' + chunk.replace(/\n/g, '↵') + '\x1b[0m');
    await sleep(4);
  }
  process.stdout.write('\n\n✅ code stream complete\n');
}

function serve(port) {
  return new Promise((resolve, reject) => {
    const server = http.createServer(async (req, res) => {
      try {
        if (req.url === '/' || req.url === '/viralforge-black-cat.html') {
          const body = await fsp.readFile(DEMO_FILE);
          res.writeHead(200, {'content-type':'text/html; charset=utf-8', 'cache-control':'no-store'});
          res.end(body);
          return;
        }
        res.writeHead(404); res.end('Not found');
      } catch (err) {
        res.writeHead(500); res.end(String(err));
      }
    });

    server.on('error', err => {
      if (err && err.code === 'EADDRINUSE' && port < BASE_PORT + 10) resolve(serve(port + 1));
      else reject(err);
    });

    server.listen(port, '0.0.0.0', () => resolve({server, port}));
  });
}

(async () => {
  await streamFile();
  const {server, port} = await serve(BASE_PORT);

  if (process.argv.includes('--smoke')) {
    const response = await fetch(`http://127.0.0.1:${port}/viralforge-black-cat.html`);
    const body = await response.text();
    if (!response.ok || !body.includes('CLAP. CLAP. CLAP.')) throw new Error('Smoke preview validation failed.');
    server.close();
    process.stdout.write('\n✅ demo smoke validation passed\n');
    return;
  }

  const url = publicUrl(port);
  process.stdout.write(`\n🐈‍⬛ Black Cat Clapping preview is live\n${url}\n\nKeep this terminal running. Ctrl+C stops the preview.\n`);
  await sleep(350);
  launchCode(['--open-url', url]);
})().catch(err => {
  console.error('\n❌ ViralForge demo failed:', err);
  process.exitCode = 1;
});
