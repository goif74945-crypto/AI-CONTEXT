import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {runInNewContext} from 'node:vm';

const source = readFileSync(new URL('../ai_ai/web/app.js', import.meta.url), 'utf8');

function boot(getUserMedia) {
  const buttons = new Map();
  const nodes = new Map();
  const element = (id) => {
    if(!nodes.has(id)) nodes.set(id, {
      id, hidden:false, disabled:false, value:'', textContent:'',
      addEventListener(name, cb) {buttons.set(`${id}:${name}`, cb);},
      replaceChildren() {}, append() {}, scrollIntoView() {},
    });
    return nodes.get(id);
  };
  const context = {
    document:{getElementById:element,createElement:()=>({textContent:'',append() {}}),createTextNode:()=>({})},
    window:{addEventListener(){}},
    navigator:{mediaDevices:{getUserMedia}},
    fetch:async()=>({ok:true,json:async()=>({token:'session',workspace:'/tmp/ws',code_run_enabled:false})}),
    performance:{now:()=>1000},
    requestAnimationFrame:()=>1,
    cancelAnimationFrame() {},
    console,
  };
  runInNewContext(source,context);
  context.showPlan({id:'f'.repeat(32),steps:[{tool:'desktop.screenshot'}],warnings:[],clap_eligible:true});
  return {buttons,element};
}

test('Emergency Stop revokes microphone pending permission', async()=>{
  let release;
  const pending = new Promise(resolve=>{release=resolve;});
  const {buttons} = boot(()=>pending);
  const armPromise=buttons.get('arm:click')();
  await buttons.get('stop:click')();
  let closed=0;
  release({getTracks:()=>[{stop:()=>{closed++;}}]});
  await armPromise;
  assert.equal(closed,1);
});

test('Discard revokes microphone pending permission', async()=>{
  let release;
  const pending=new Promise(resolve=>{release=resolve;});
  const {buttons}=boot(()=>pending);
  const armPromise=buttons.get('arm:click')();
  buttons.get('discard:click')();
  let closed=0;
  release({getTracks:()=>[{stop:()=>{closed++;}}]});
  await armPromise;
  assert.equal(closed,1);
});
