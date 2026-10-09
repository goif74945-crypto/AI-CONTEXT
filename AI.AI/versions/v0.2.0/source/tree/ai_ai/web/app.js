"use strict";
const $ = (id) => document.getElementById(id);
let token = null;
let plan = null;
let clapStream = null;
let clapCtx = null;
let clapFrame = null;
let clapUntil = 0;
let clapLast = 0;
let clapCount = 0;
let clapAbove = false;
const display = (text) => { $("output").textContent = typeof text === "string" ? text : JSON.stringify(text, null, 2); };
async function api(path, method="GET", body) {
  const res = await fetch(path,{method,cache:"no-store",headers:{"Content-Type":"application/json",...(token ? {"X-AI-AI-TOKEN":token}: {})}, ...(body !== undefined ? {body:JSON.stringify(body)}:{})});
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || `HTTP ${res.status}`);
  return data;
}
async function init() {
  try {
    const s=await api("/api/session"); token=s.token;
    display(`Local agent ready.\nWorkspace: ${s.workspace}\nTrusted code run: ${s.code_run_enabled ? "ENABLED" : "DISABLED"}\nUse Generate plan to start.`);
  } catch(e){display(`Connection error: ${e.message}`);}
}
function showPlan(value) {
  plan=value;
  $("planBox").hidden=false;
  const box=$("steps"); box.replaceChildren();
  for (const step of value.steps){const li=document.createElement("li"); const strong=document.createElement("strong");strong.textContent=step.tool+"  ";li.append(strong,document.createTextNode(JSON.stringify(step)));box.append(li);}
  $("warnings").textContent=value.warnings.join(" ");
  $("arm").disabled=!value.clap_eligible;
  $("arm").title=value.clap_eligible?"Double-clap will execute this single reviewed plan":"High-risk actions cannot be clap-triggered";
  $("planBox").scrollIntoView({behavior:"smooth",block:"center"});
}
$("plan").addEventListener("click",async()=>{
  cancelClap(); try {const request={text:$("command").value,use_ai:$("aiMode").checked,share_screen_text:$("screenContext").checked};showPlan(await api("/api/plan","POST",request));display("Plan ready. Approval required before execution.");}
  catch(e){display(`Planning failed: ${e.message}`);}
});
async function execute(){
  cancelClap(); if(!plan)return;
  const selected=plan;plan=null;$("planBox").hidden=true;
  display("Executing approved plan...");
  try {const out=await api("/api/execute","POST",{plan_id:selected.id,approval:"I_APPROVE_THIS_PLAN"});display(out);}
  catch(e){display(`Execution failed: ${e.message}`);}
}
$("execute").addEventListener("click",execute);
$("discard").addEventListener("click",()=>{plan=null;$("planBox").hidden=true;cancelClap();display("Plan discarded. It will expire on the server.");});
$("stop").addEventListener("click",async()=>{
  cancelClap();try{display(await api("/api/stop","POST",{}));}catch(e){display(e.message);}
});
const Recognition=window.SpeechRecognition||window.webkitSpeechRecognition;
$("voice").addEventListener("click",()=>{
  if(!Recognition){display("Speech recognition unavailable in this browser. Use typing or a browser supporting Web Speech API.");return;}
  try{const r=new Recognition();r.lang="th-TH";r.interimResults=false;r.maxAlternatives=1;r.onresult=(event)=>{$("command").value=event.results[0][0].transcript;display("Speech captured. Review/Generate plan before execution.");};r.onerror=(e)=>display(`Microphone/speech error: ${e.error}`);r.start();display("Listening... Speak your command.");}
  catch(e){display(`Cannot start speech recognition: ${e.message}`);}
});
function cancelClap(){
  clapUntil=0;$("armedNote").hidden=true;
  if(clapFrame!==null){cancelAnimationFrame(clapFrame);clapFrame=null;}
  if(clapStream){clapStream.getTracks().forEach(t=>t.stop());clapStream=null;}
  if(clapCtx){clapCtx.close().catch(()=>{});clapCtx=null;}
}
$("arm").addEventListener("click",async()=>{
  if(!plan||!plan.clap_eligible){display("This plan cannot be clap-triggered.");return;}
  cancelClap();
  try{
    clapStream=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:false,noiseSuppression:false,autoGainControl:false},video:false});
    clapCtx=new(window.AudioContext||window.webkitAudioContext)();
    const src=clapCtx.createMediaStreamSource(clapStream);
    const hp=clapCtx.createBiquadFilter();hp.type="highpass";hp.frequency.value=1250;
    const analyzer=clapCtx.createAnalyser();analyzer.fftSize=1024;src.connect(hp);hp.connect(analyzer);
    const data=new Float32Array(analyzer.fftSize);
    clapUntil=performance.now()+30000;clapLast=0;clapCount=0;clapAbove=false;
    $("armedNote").hidden=false;display("Double-clap armed for 30 seconds. Clap twice, about 0.2-0.9 seconds apart.");
    const sample=()=>{
      if(!plan||performance.now()>clapUntil){cancelClap();return;}
      analyzer.getFloatTimeDomainData(data);
      let energy=0;for(let i=0;i<data.length;i++)energy+=data[i]*data[i];
      const rms=Math.sqrt(energy/data.length); const now=performance.now();
      // Prototype transient detector; requires microphone calibration for reliable production use.
      if(rms>.14&&!clapAbove&&now-clapLast>170){
        if(clapLast&&now-clapLast<950)clapCount++;else clapCount=1;
        clapLast=now;
        if(clapCount>=2){cancelClap();execute();return;}
      }
      clapAbove=rms>.10;
      clapFrame=requestAnimationFrame(sample);
    };
    sample();
  }catch(e){cancelClap();display(`Microphone could not be armed: ${e.message}`);}
});
window.addEventListener("beforeunload",cancelClap);
init();
