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
    if (action === 'Install + Studio') terminal(dir,'npm install && npm run dev','ViralForge Studio');
    if (action === 'Render Now') terminal(dir,'npm install && npm run render','ViralForge Render');
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
    terminal(root,'npm run ' + script,name);
  } catch (error) {
    vscode.window.showErrorMessage('ViralForge: ' + (error instanceof Error ? error.message : String(error)));
  }
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('viralForge.createShortProject',createProject),
    vscode.commands.registerCommand('viralForge.openStudio',()=>run('dev','ViralForge Studio')),
    vscode.commands.registerCommand('viralForge.renderShort',()=>run('render','ViralForge Render'))
  );
}

function deactivate() {}

module.exports = {activate,deactivate};
