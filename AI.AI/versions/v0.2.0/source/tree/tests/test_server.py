from fastapi.testclient import TestClient
from ai_ai.server import make_app, PORT
from ai_ai.executor import Executor,ActionError

class FakeExecutor(Executor):
    def __init__(self,workspace):
        super().__init__(workspace)
        self.actions=[]
    def perform(self,step,cancel):
        self.actions.append(step.tool)
        return "mock: "+step.tool

def setup(tmp_path):
    executor=FakeExecutor(tmp_path)
    client=TestClient(make_app(tmp_path,executor=executor))
    token=client.get("/api/session").json()["token"]
    return client, {"X-AI-AI-TOKEN":token}, executor

def test_readiness(tmp_path):
    c,h,e=setup(tmp_path)
    assert c.get("/").status_code==200
    assert "text/html" in c.get("/").headers["content-type"]
    assert "javascript" in c.get("/app.js").headers["content-type"]
    assert c.get("/api/status").json()["bind"]=="loopback-only"

def test_requires_auth(tmp_path):
    c,h,e=setup(tmp_path)
    assert c.post("/api/plan",json={"text":"screenshot"}).status_code==401
    assert c.post("/api/execute",json={"plan_id":"0"*32,"approval":"I_APPROVE_THIS_PLAN"}).status_code==401

def test_plan_never_executes_itself(tmp_path):
    c,h,e=setup(tmp_path)
    r=c.post("/api/plan",headers=h,json={"text":"click 4 5"})
    assert r.status_code==200
    p=r.json()
    assert p["clap_eligible"] is False
    assert e.actions==[]
    result=c.post("/api/execute",headers=h,json={"plan_id":p["id"],"approval":"I_APPROVE_THIS_PLAN"})
    assert result.json()["status"]=="PASS"
    assert e.actions==["desktop.click"]
    assert c.post("/api/execute",headers=h,json={"plan_id":p["id"],"approval":"I_APPROVE_THIS_PLAN"}).status_code==409

def test_approval_literal_required(tmp_path):
    c,h,e=setup(tmp_path)
    pid=c.post("/api/plan",headers=h,json={"text":"screenshot"}).json()["id"]
    assert c.post("/api/execute",headers=h,json={"plan_id":pid,"approval":"YES"}).status_code==422
    assert e.actions==[]

def test_bad_plan_and_extra_fields(tmp_path):
    c,h,e=setup(tmp_path)
    assert c.post("/api/plan",headers=h,json={"text":"hack phone"}).status_code==422
    assert c.post("/api/plan",headers=h,json={"text":"screenshot","shell":"rm -rf /"}).status_code==422

def test_host_deny(tmp_path):
    c,h,e=setup(tmp_path)
    assert c.get("/",headers={"Host":"attacker.example"}).status_code==403

def test_cross_origin_deny(tmp_path):
    c,h,e=setup(tmp_path)
    headers={**h,"Host":f"127.0.0.1:{PORT}","Origin":"https://attacker.example"}
    assert c.post("/api/plan",headers=headers,json={"text":"screenshot"}).status_code==403

def test_multistep_failure_stops(tmp_path):
    c,h,e=setup(tmp_path)
    def fail_on_second(step,cancel):
        if step.tool=="desktop.type":raise ActionError("mock failure")
        e.actions.append(step.tool)
        return "fine"
    e.perform=fail_on_second
    pid=c.post("/api/plan",headers=h,json={"text":"screenshot\ntype hello\nscreenshot"}).json()["id"]
    out=c.post("/api/execute",headers=h,json={"plan_id":pid,"approval":"I_APPROVE_THIS_PLAN"}).json()
    assert out["status"]=="FAIL" and out["failed_index"]==1
    assert e.actions==["desktop.screenshot"]

def test_stop_endpoint(tmp_path):
    c,h,e=setup(tmp_path)
    assert c.post("/api/stop",headers=h,json={}).json()["stop_requested"] is True

def test_no_api_key_is_explicit_error(tmp_path,monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    c,h,e=setup(tmp_path)
    response=c.post("/api/plan",headers=h,json={"text":"hello","use_ai":True})
    assert response.status_code==422 and "OPENAI_API_KEY" in response.json()["detail"]
