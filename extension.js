const vscode = require('vscode');
const fs = require('fs/promises');
const path = require('path');

const REMOTION_VERSION = '4.0.527';
const PRESETS = {
  TikTok: 'out/tiktok.mp4',
  'Instagram Reels': 'out/reels.mp4',
  'YouTube Shorts': 'out/shorts.mp4'
};

function cleanName(value) {
  return value.trim().toLowerCase().replace(/[^a-z0-9-_]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 64);
}

function pkg(name, output) {
  return JSON.stringify({
    name,
    private: true,
    version: '0.1.0',
    scripts: {
      dev: 'remotion studio src/index.ts',
      render: 'remotion render src/index.ts ViralShort ' + output + ' --codec=h264 --crf=18',
      preview: 'remotion render src/index.ts ViralShort out/preview.mp4 --codec=h264 --crf=23 --frames=0-299'
    },
    dependencies: {
      '@remotion/cli': REMOTION_VERSION,
      remotion: REMOTION_VERSION,
      react: '18.3.1',
      'react-dom': '18.3.1'
    },
    devDependencies: {
      '@types/react': '18.3.12',
      '@types/react-dom': '18.3.1',
      typescript: '5.7.2'
    }
  }, null, 2) + '\n';
}

function tsconfig() {
  return JSON.stringify({
    compilerOptions: {
      target: 'ES2022',
      lib: ['DOM', 'ES2022'],
      jsx: 'react-jsx',
      module: 'ESNext',
      moduleResolution: 'Bundler',
      strict: true,
      skipLibCheck: true,
      noEmit: true
    },
    include: ['src']
  }, null, 2) + '\n';
}

function indexTs() {
  return [
    "import {registerRoot} from 'remotion';",
    "import {Root} from './Root';",
    '',
    'registerRoot(Root);',
    ''
  ].join('\n');
}

function rootTsx() {
  return [
    "import React from 'react';",
    "import {Composition} from 'remotion';",
    "import {ViralShort} from './ViralShort';",
    '',
    'export const Root: React.FC = () => (',
    '  <Composition',
    '    id="ViralShort"',
    '    component={ViralShort}',
    '    durationInFrames={900}',
    '    fps={60}',
    '    width={1080}',
    '    height={1920}',
    '  />',
    ');',
    ''
  ].join('\n');
}

function videoTsx(title, subtitle, accent) {
  return [
    "import React from 'react';",
    "import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';",
    '',
    'const TITLE = ' + JSON.stringify(title) + ';',
    'const SUBTITLE = ' + JSON.stringify(subtitle) + ';',
    'const ACCENT = ' + JSON.stringify(accent) + ';',
    '',
    'const particles = Array.from({length: 44}, (_, i) => ({',
    '  x: (i * 173 + 71) % 1080,',
    '  y: (i * 311 + 197) % 1920,',
    '  s: 3 + (i % 7) * 2,',
    '  speed: 0.25 + (i % 5) * 0.08,',
    '}));',
    '',
    'const Particle: React.FC<{i: number}> = ({i}) => {',
    '  const frame = useCurrentFrame();',
    '  const p = particles[i];',
    '  const y = (p.y - frame * p.speed * 8 + 2200) % 2200 - 140;',
    '  const x = p.x + Math.sin((frame + i * 13) / 18) * (18 + (i % 8) * 5);',
    '  return <div style={{position:"absolute",left:x,top:y,width:p.s,height:p.s,borderRadius:999,background:ACCENT,boxShadow:"0 0 " + (p.s * 5) + "px " + ACCENT,opacity:0.18 + ((i * 37) % 55) / 100}} />;',
    '};',
    '',
    'const Hook: React.FC = () => {',
    '  const frame = useCurrentFrame();',
    '  const {fps} = useVideoConfig();',
    '  const enter = spring({frame,fps,config:{damping:13,stiffness:180,mass:0.7}});',
    '  const punch = interpolate(frame,[0,8,18,30],[1.18,0.94,1.04,1],{extrapolateLeft:"clamp",extrapolateRight:"clamp"});',
    '  const shake = frame < 22 ? Math.sin(frame * 2.7) * (22 - frame) * 0.7 : 0;',
    '  return <AbsoluteFill style={{alignItems:"center",justifyContent:"center"}}><div style={{transform:"translateX(" + shake + "px) scale(" + (enter * punch) + ")",textAlign:"center",padding:"0 72px"}}><div style={{fontFamily:"Arial Black,Arial,sans-serif",fontSize:116,lineHeight:0.93,letterSpacing:-6,color:"#fff",textTransform:"uppercase",textShadow:"0 0 24px " + ACCENT + ",0 10px 50px rgba(0,0,0,.8)"}}>{TITLE}</div><div style={{marginTop:36,fontFamily:"Arial,sans-serif",fontWeight:800,fontSize:43,letterSpacing:2,color:ACCENT}}>{SUBTITLE}</div></div></AbsoluteFill>;',
    '};',
    '',
    'const Card: React.FC<{h:string;d:string;i:number}> = ({h,d,i}) => {',
    '  const frame = useCurrentFrame();',
    '  const {fps} = useVideoConfig();',
    '  const reveal = spring({frame:Math.max(0,frame-i*20),fps,config:{damping:15,stiffness:170,mass:0.8}});',
    '  return <div style={{transform:"translateX(" + interpolate(reveal,[0,1],[190,0]) + "px)",opacity:reveal,width:820,padding:"34px 42px",border:"2px solid " + ACCENT + "80",borderRadius:30,background:"rgba(8,12,20,.76)",boxShadow:"0 0 34px " + ACCENT + "20"}}><div style={{fontFamily:"Arial Black,Arial,sans-serif",fontSize:54,color:"#fff"}}>{h}</div><div style={{marginTop:10,fontFamily:"Arial,sans-serif",fontSize:30,fontWeight:700,color:"#bac7d9"}}>{d}</div></div>;',
    '};',
    '',
    'const Core: React.FC = () => <AbsoluteFill style={{alignItems:"center",justifyContent:"center",gap:30}}><Card i={0} h="HOOK FAST" d="0.0\u20131.0s: stop the scroll."/><Card i={1} h="MOTION HARD" d="Punch zoom + kinetic typography."/><Card i={2} h="EXPORT CLEAN" d="1080\u00d71920 \u2022 60 FPS \u2022 H.264"/></AbsoluteFill>;',
    '',
    'const Finale: React.FC = () => {',
    '  const frame = useCurrentFrame();',
    '  const {fps} = useVideoConfig();',
    '  const pop = spring({frame,fps,config:{damping:10,stiffness:140,mass:0.65}});',
    '  return <AbsoluteFill style={{alignItems:"center",justifyContent:"center"}}><div style={{transform:"scale(" + pop + ")",textAlign:"center"}}><div style={{fontFamily:"Arial Black,Arial,sans-serif",fontSize:98,lineHeight:0.95,color:"#fff",textShadow:"0 0 30px " + ACCENT}}>BUILT IN<br/>VS CODE</div><div style={{marginTop:32,color:ACCENT,fontFamily:"Arial,sans-serif",fontWeight:900,fontSize:42}}>RENDER. POST. REPEAT.</div></div></AbsoluteFill>;',
    '};',
    '',
    'export const ViralShort: React.FC = () => {',
    '  const frame = useCurrentFrame();',
    '  const glow = 0.14 + Math.sin(frame / 20) * 0.04;',
    '  return <AbsoluteFill style={{overflow:"hidden",background:"radial-gradient(circle at 50% 22%,#17233a 0%,#070a10 38%,#020305 100%)"}}><AbsoluteFill style={{opacity:glow,background:"radial-gradient(circle at 50% 45%," + ACCENT + " 0%,transparent 48%)"}}/>{particles.map((_,i)=><Particle key={i} i={i}/>)}<Sequence from={0} durationInFrames={250}><Hook/></Sequence><Sequence from={220} durationInFrames={420}><Core/></Sequence><Sequence from={650} durationInFrames={250}><Finale/></Sequence></AbsoluteFill>;',
    '};',
    ''
  ].join('\n');
}

function catDemoHtml() {
  return [
    '<!doctype html>',
    '<html lang="en">',
    '<head>',
    '<meta charset="utf-8">',
    '<meta name="viewport" content="width=device-width,initial-scale=1">',
    '<title>ViralForge Black Cat Clapping</title>',
    '<style>',
    '*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#020305;color:#fff;font-family:Arial,Helvetica,sans-serif}',
    'body{display:grid;place-items:center;background:radial-gradient(circle at 50% 20%,#17233a 0,#080a10 42%,#020305 100%)}',
    '.frame{position:relative;height:min(96vh,960px);aspect-ratio:9/16;overflow:hidden;border-radius:28px;background:radial-gradient(circle at 50% 46%,rgba(0,229,255,.22),transparent 40%),linear-gradient(180deg,#070a10,#020305);box-shadow:0 0 90px rgba(0,229,255,.18),0 30px 100px #000}',
    '.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,229,255,.06) 1px,transparent 1px),linear-gradient(90deg,rgba(0,229,255,.06) 1px,transparent 1px);background-size:38px 38px;mask-image:linear-gradient(to bottom,transparent,#000 24%,#000 80%,transparent)}',
    '.rain{position:absolute;inset:-25% 0 0;opacity:.18;filter:blur(.2px);font:700 12px/1.65 Consolas,monospace;color:#00e5ff;white-space:pre;transform:rotate(-5deg) scale(1.25);animation:rain 4s linear infinite}',
    '@keyframes rain{to{transform:translateY(180px) rotate(-5deg) scale(1.25)}}',
    '.badge{position:absolute;top:4.5%;left:6%;padding:10px 16px;border:1px solid rgba(0,229,255,.65);border-radius:999px;background:rgba(0,0,0,.48);font-weight:900;font-size:14px;letter-spacing:2px;color:#72f6ff;box-shadow:0 0 24px rgba(0,229,255,.14)}',
    '.title{position:absolute;z-index:5;top:10%;left:7%;right:7%;font:900 clamp(28px,5.2vh,64px)/.9 "Arial Black",Arial,sans-serif;letter-spacing:-2px;text-transform:uppercase;text-shadow:0 0 22px #00e5ff,0 8px 28px #000;animation:titlePunch .7s cubic-bezier(.18,.85,.2,1.15) both}',
    '.title span{color:#00e5ff}',
    '@keyframes titlePunch{0%{transform:scale(1.55) rotate(-4deg);opacity:0}60%{transform:scale(.96) rotate(1deg)}100%{transform:scale(1);opacity:1}}',
    '.catWrap{position:absolute;left:50%;top:54%;width:82%;transform:translate(-50%,-50%);filter:drop-shadow(0 35px 35px rgba(0,0,0,.8));animation:catIn .55s .35s cubic-bezier(.2,.9,.25,1.25) both}',
    '@keyframes catIn{from{transform:translate(-50%,-42%) scale(.6);opacity:0}to{transform:translate(-50%,-50%) scale(1);opacity:1}}',
    'svg{display:block;width:100%;height:auto;overflow:visible}',
    '#leftArm{transform-box:view-box;transform-origin:168px 455px;animation:leftClap .34s ease-in-out infinite alternate}',
    '#rightArm{transform-box:view-box;transform-origin:332px 455px;animation:rightClap .34s ease-in-out infinite alternate}',
    '@keyframes leftClap{0%{transform:rotate(-22deg) translate(-18px,14px)}100%{transform:rotate(18deg) translate(38px,-5px)}}',
    '@keyframes rightClap{0%{transform:rotate(22deg) translate(18px,14px)}100%{transform:rotate(-18deg) translate(-38px,-5px)}}',
    '#clapFlash{transform-box:fill-box;transform-origin:center;animation:flash .34s ease-in-out infinite alternate}',
    '@keyframes flash{0%,52%{opacity:0;transform:scale(.3)}100%{opacity:.95;transform:scale(1.7)}}',
    '#head{transform-box:fill-box;transform-origin:center;animation:headBob .68s ease-in-out infinite alternate}',
    '@keyframes headBob{to{transform:translateY(5px) rotate(1.7deg)}}',
    '.caption{position:absolute;z-index:6;left:5%;right:5%;bottom:7%;text-align:center;font:900 clamp(19px,3.2vh,38px)/1.04 "Arial Black",Arial,sans-serif;text-transform:uppercase;letter-spacing:-.5px;text-shadow:0 4px 18px #000,0 0 14px #000}',
    '.caption b{display:inline-block;color:#00e5ff;animation:pulse .68s ease-in-out infinite alternate}',
    '@keyframes pulse{to{transform:scale(1.08);text-shadow:0 0 18px #00e5ff}}',
    '.scan{position:absolute;inset:0;pointer-events:none;background:linear-gradient(transparent 0 48%,rgba(255,255,255,.035) 50%,transparent 52%);background-size:100% 8px;mix-blend-mode:screen;opacity:.45}',
    '.flashScreen{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none;animation:screenFlash .68s ease-in-out infinite}',
    '@keyframes screenFlash{0%,42%,100%{opacity:0}50%{opacity:.055}}',
    '</style>',
    '</head>',
    '<body>',
    '<main class="frame">',
    '<div class="grid"></div>',
    '<div class="rain">const viral = true;\\nrender(frame);\\nCAT.clap();\\nwhile(hype){ship();}\\n010101101010\\nAI → CODE → MOTION\\nconst fps = 60;\\nrender(frame);\\nCAT.clap();\\nwhile(hype){ship();}\\n010101101010\\nAI → CODE → MOTION</div>',
    '<div class="badge">VIRALFORGE // LIVE</div>',
    '<div class="title">WHEN THE CODE<br><span>FINALLY RUNS</span></div>',
    '<div class="catWrap">',
    '<svg viewBox="0 0 500 760" role="img" aria-label="Original animated black cat clapping">',
    '<defs><radialGradient id="fur" cx="45%" cy="30%"><stop offset="0" stop-color="#30343a"/><stop offset=".55" stop-color="#111318"/><stop offset="1" stop-color="#050607"/></radialGradient><radialGradient id="palm"><stop offset="0" stop-color="#d7b69d"/><stop offset="1" stop-color="#9f7b67"/></radialGradient></defs>',
    '<ellipse cx="250" cy="720" rx="150" ry="25" fill="#000" opacity=".65"/>',
    '<ellipse cx="250" cy="505" rx="128" ry="176" fill="url(#fur)"/>',
    '<g id="head"><path d="M145 228 L168 120 L226 184 Z" fill="#0a0b0e"/><path d="M355 228 L332 120 L274 184 Z" fill="#0a0b0e"/><path d="M167 170 L178 136 L204 180 Z" fill="#5d3447" opacity=".7"/><path d="M333 170 L322 136 L296 180 Z" fill="#5d3447" opacity=".7"/><ellipse cx="250" cy="257" rx="122" ry="108" fill="url(#fur)"/><ellipse cx="207" cy="241" rx="24" ry="15" fill="#91ff90"/><ellipse cx="293" cy="241" rx="24" ry="15" fill="#91ff90"/><ellipse cx="207" cy="241" rx="6" ry="14" fill="#090b0c"/><ellipse cx="293" cy="241" rx="6" ry="14" fill="#090b0c"/><path d="M242 277 Q250 285 258 277 Q250 295 242 277" fill="#c4888f"/><path d="M188 296 Q250 350 312 296 Q303 365 250 369 Q197 365 188 296Z" fill="#efe9df"/><path d="M202 315 Q250 346 298 315" fill="none" stroke="#34343a" stroke-width="5" stroke-linecap="round"/><path d="M206 329 L211 345 M229 338 L232 354 M271 338 L268 354 M294 329 L289 345" stroke="#aaa39a" stroke-width="3"/></g>',
    '<path d="M142 410 Q95 480 132 610" fill="none" stroke="#0a0c10" stroke-width="58" stroke-linecap="round"/>',
    '<path d="M358 410 Q405 480 368 610" fill="none" stroke="#0a0c10" stroke-width="58" stroke-linecap="round"/>',
    '<g id="leftArm"><path d="M168 430 Q120 498 188 550" fill="none" stroke="#11141a" stroke-width="54" stroke-linecap="round"/><g transform="translate(184 548) rotate(-18)"><ellipse cx="0" cy="0" rx="44" ry="52" fill="url(#palm)"/><rect x="-47" y="-62" width="17" height="65" rx="9" fill="#c8a58e"/><rect x="-27" y="-72" width="17" height="70" rx="9" fill="#d2af96"/><rect x="-6" y="-75" width="17" height="72" rx="9" fill="#d8b69c"/><rect x="15" y="-66" width="17" height="64" rx="9" fill="#caa58e"/></g></g>',
    '<g id="rightArm"><path d="M332 430 Q380 498 312 550" fill="none" stroke="#11141a" stroke-width="54" stroke-linecap="round"/><g transform="translate(316 548) rotate(18)"><ellipse cx="0" cy="0" rx="44" ry="52" fill="url(#palm)"/><rect x="30" y="-62" width="17" height="65" rx="9" fill="#c8a58e"/><rect x="10" y="-72" width="17" height="70" rx="9" fill="#d2af96"/><rect x="-11" y="-75" width="17" height="72" rx="9" fill="#d8b69c"/><rect x="-32" y="-66" width="17" height="64" rx="9" fill="#caa58e"/></g></g>',
    '<circle id="clapFlash" cx="250" cy="542" r="20" fill="#fff"/><circle cx="250" cy="542" r="48" fill="none" stroke="#00e5ff" stroke-width="4" opacity=".35"/>',
    '</svg>',
    '</div>',
    '<div class="caption">AI AFTER ONE SUCCESSFUL BUILD<br><b>👏 CLAP. CLAP. CLAP.</b></div>',
    '<div class="scan"></div><div class="flashScreen"></div>',
    '</main>',
    '</body>',
    '</html>'
  ].join('\\n');
}

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function streamCodeIntoEditor(filePath, source) {
  await fs.writeFile(filePath, '', 'utf8');
  const uri = vscode.Uri.file(filePath);
  const document = await vscode.workspace.openTextDocument(uri);
  const editor = await vscode.window.showTextDocument(document, {
    viewColumn: vscode.ViewColumn.One,
    preview: false,
    preserveFocus: false
  });

  const chunkSize = 180;
  for (let i = 0; i < source.length; i += chunkSize) {
    const chunk = source.slice(i, i + chunkSize);
    const lastLine = document.lineAt(document.lineCount - 1);
    const end = lastLine.range.end;
    const edit = new vscode.WorkspaceEdit();
    edit.insert(uri, end, chunk);
    const ok = await vscode.workspace.applyEdit(edit);
    if (!ok) throw new Error('VS Code rejected a live-code edit.');
    const nowLast = document.lineAt(document.lineCount - 1);
    editor.revealRange(new vscode.Range(nowLast.range.end, nowLast.range.end), vscode.TextEditorRevealType.InCenterIfOutsideViewport);
    await delay(5);
  }
  await document.save();
  return document;
}

function openCatPreview(source) {
  const panel = vscode.window.createWebviewPanel(
    'viralForgeBlackCat',
    'ViralForge • Black Cat Clapping',
    vscode.ViewColumn.Beside,
    {enableScripts: false, retainContextWhenHidden: true}
  );
  panel.webview.html = source;
  return panel;
}

async function runTrendingCatDemo() {
  const root = rootFolder();
  if (!root) {
    return vscode.window.showErrorMessage('ViralForge: Open any folder first, then run the cat demo.');
  }

  const target = path.join(root, 'viralforge-black-cat-demo.html');
  const source = catDemoHtml();

  await vscode.window.withProgress(
    {
      location: vscode.ProgressLocation.Notification,
      title: 'ViralForge: firing live code → viral cat',
      cancellable: false
    },
    async progress => {
      progress.report({message: 'opening file and streaming code…'});
      await streamCodeIntoEditor(target, source);
      progress.report({message: 'launching 9:16 preview…'});
      await delay(120);
      openCatPreview(source);
    }
  );

  vscode.window.setStatusBarMessage('$(flame) ViralForge: Black Cat Clapping is live', 5000);
}

async function ensureTarget(dir) {
  try {
    const entries = await fs.readdir(dir);
    if (entries.length) throw new Error('Target folder already exists and is not empty.');
  } catch (error) {
    if (error && error.code === 'ENOENT') {
      await fs.mkdir(dir, {recursive:true});
      return;
    }
    throw error;
  }
}

async function writeProject(dir, config) {
  await fs.mkdir(path.join(dir, 'src'), {recursive:true});
  await fs.writeFile(path.join(dir, 'package.json'), pkg(config.name, config.output));
  await fs.writeFile(path.join(dir, 'tsconfig.json'), tsconfig());
  await fs.writeFile(path.join(dir, 'src', 'index.ts'), indexTs());
  await fs.writeFile(path.join(dir, 'src', 'Root.tsx'), rootTsx());
  await fs.writeFile(path.join(dir, 'src', 'ViralShort.tsx'), videoTsx(config.title, config.subtitle, config.accent));
  await fs.writeFile(path.join(dir, '.gitignore'), 'node_modules/\nout/\n');
  await fs.writeFile(path.join(dir, 'README.md'), '# ViralForge Short\n\nRun npm install, then npm run dev. Render with npm run render.\n');
}

function rootFolder() {
  const folders = vscode.workspace.workspaceFolders;
  return folders && folders[0] ? folders[0].uri.fsPath : null;
}

function npmCommand() {
  return process.platform === 'win32' ? 'npm.cmd' : 'npm';
}

function terminal(cwd, command, name) {
  const t = vscode.window.createTerminal({name,cwd});
  t.show(true);
  t.sendText(command,true);
}

async function createProject() {
  const root = rootFolder();
  if (!root) return vscode.window.showErrorMessage('ViralForge: Open a folder first.');

  const platform = await vscode.window.showQuickPick(Object.keys(PRESETS), {placeHolder:'Target platform',ignoreFocusOut:true});
  if (!platform) return;

  const raw = await vscode.window.showInputBox({prompt:'Project folder name',value:'viral-short',ignoreFocusOut:true});
  if (!raw) return;
  const name = cleanName(raw);
  if (!name) return vscode.window.showErrorMessage('ViralForge: Invalid project name.');

  const title = await vscode.window.showInputBox({prompt:'Main hook',value:'THIS WAS BUILT BY AI',ignoreFocusOut:true});
  if (!title) return;
  const subtitle = await vscode.window.showInputBox({prompt:'Subtitle',value:'CODE \u2192 MOTION \u2192 VIDEO',ignoreFocusOut:true});
  if (!subtitle) return;
  const accent = await vscode.window.showInputBox({prompt:'Accent hex',value:'#00E5FF',validateInput:v=>/^#[0-9A-Fa-f]{6}$/.test(v)?null:'Use #RRGGBB',ignoreFocusOut:true});
  if (!accent) return;

  const dir = path.join(root,name);
  try {
    await ensureTarget(dir);
    await writeProject(dir,{name,output:PRESETS[platform],title,subtitle,accent});
    const action = await vscode.window.showInformationMessage('ViralForge created ' + name + ' for ' + platform + '.', 'Install + Studio', 'Render Now');
    if (action === 'Install + Studio') terminal(dir,npmCommand() + ' install && ' + npmCommand() + ' run dev','ViralForge Studio');
    if (action === 'Render Now') terminal(dir,npmCommand() + ' install && ' + npmCommand() + ' run render','ViralForge Render');
  } catch (error) {
    vscode.window.showErrorMessage('ViralForge failed: ' + (error instanceof Error ? error.message : String(error)));
  }
}

async function run(script,name) {
  const root = rootFolder();
  if (!root) return vscode.window.showErrorMessage('ViralForge: Open the generated project folder first.');
  try {
    const data = JSON.parse(await fs.readFile(path.join(root,'package.json'),'utf8'));
    if (!data.scripts || !data.scripts[script]) return vscode.window.showErrorMessage('ViralForge: Missing npm script ' + script + '.');
    terminal(root,npmCommand() + ' run ' + script,name);
  } catch (error) {
    vscode.window.showErrorMessage('ViralForge: ' + (error instanceof Error ? error.message : String(error)));
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('viralForge.createShortProject',createProject),
    vscode.commands.registerCommand('viralForge.openStudio',()=>run('dev','ViralForge Studio')),
    vscode.commands.registerCommand('viralForge.renderShort',()=>run('render','ViralForge Render')),
    vscode.commands.registerCommand('viralForge.runTrendingCatDemo',runTrendingCatDemo)
  );
}

function deactivate() {}

module.exports = {activate,deactivate};
