import json
import os
import pytest
import subprocess
from pathlib import Path
from pydantic import ValidationError
from fastapi.testclient import TestClient
from ai_ai.contracts import ProposedPlan, PlanRequest
from ai_ai.executor import Executor, ActionError
from ai_ai.planner import parse_rules
from ai_ai.server import make_app
from ai_ai.audit import AuditLog
import threading


def step(**kw):
    return ProposedPlan.model_validate({"steps":[kw]}).steps[0]

@pytest.mark.parametrize("instruction,expected",[
    ("คลิกข้อความ Save", "desktop.click_text"),
    ("click text Submit", "desktop.click_text"),
    ("ตรวจข้อความ Ready", "desktop.assert_text"),
    ("รอข้อความ Ready :: 3", "desktop.wait_text"),
    ("มือถือปัด 100 900 100 200", "android.swipe"),
    ("android swipe 100 900 100 200 500", "android.swipe"),
    ("มือถือกด BACK", "android.keyevent"),
    ("android tap text Settings", "android.tap_text"),
    ("android assert text Settings", "android.assert_text"),
    ("android screenshot", "android.screenshot"),
])
def test_more_commands(instruction,expected):
    assert parse_rules(instruction).steps[0].tool==expected

@pytest.mark.parametrize("payload",[
    {"tool":"android.keyevent","key":"POWER"},
    {"tool":"android.swipe","x1":1,"y1":1,"x2":3,"y2":3,"duration_ms":5},
    {"tool":"android.tap_text","text":"Save","serial":"X; echo pwned"},
    {"tool":"android.screenshot","serial":"bad serial"},
    {"tool":"desktop.wait_text","text":"Save","timeout_seconds":60},
    {"tool":"desktop.click_text","text":""},
])
def test_invalid_tools_fail_closed(payload):
    with pytest.raises(ValidationError): step(**payload)


def test_screen_optin_only_with_ai():
    with pytest.raises(ValidationError): PlanRequest(text="hello",share_screen_text=True)
    assert PlanRequest(text="hello",use_ai=True,share_screen_text=True).share_screen_text


def test_screen_optin_fails_without_local_ocr(monkeypatch,tmp_path):
    class Unavailable(Executor):
        def read_screen_evidence(self):
            from ai_ai.vision import VisionError
            raise VisionError("OCR not installed")
    e=Unavailable(tmp_path)
    c=TestClient(make_app(tmp_path,executor=e))
    token=c.get("/api/session").json()["token"]
    out=c.post("/api/plan",headers={"X-AI-AI-TOKEN":token},
               json={"text":"click Save", "use_ai":True,"share_screen_text":True})
    assert out.status_code==422 and "OCR not installed" in out.json()["detail"]


def test_history_authenticated_no_command_contents(tmp_path):
    c=TestClient(make_app(tmp_path))
    assert c.get("/api/history").status_code==401
    h={"X-AI-AI-TOKEN":c.get("/api/session").json()["token"]}
    response=c.post("/api/plan",headers=h,json={"text":"พิมพ์ MY_SECRET_EXAMPLE"})
    assert response.status_code==200
    history=c.get("/api/history",headers=h)
    assert history.status_code==200
    assert history.json()["events"][0]["event"]=="PLAN_CREATED"
    assert "MY_SECRET_EXAMPLE" not in history.text
    assert "MY_SECRET_EXAMPLE" not in (tmp_path/"execution-audit.jsonl").read_text()


def test_audit_log_refuses_symlink(tmp_path):
    outside=tmp_path/"outside"
    outside.write_text("protected")
    audit=AuditLog(tmp_path)
    try: audit.path.symlink_to(outside)
    except (OSError,NotImplementedError): pytest.skip("Platform blocks symlinks")
    if hasattr(os,"O_NOFOLLOW"):
        with pytest.raises(OSError): audit.record("PLAN_CREATED",plan_id="fake")
        assert outside.read_text()=="protected"


def test_android_swipe_exact_argv(monkeypatch,tmp_path):
    from ai_ai import executor as module
    commands=[]
    monkeypatch.setattr(module.shutil,"which", lambda _:"/adb")
    def fake_run(argv,**kwargs):
        commands.append(argv)
        text="List of devices attached\nONE\tdevice\n" if argv[-1]=="devices" else "OK"
        return subprocess.CompletedProcess(argv,0,stdout=text,stderr="")
    monkeypatch.setattr(module.subprocess,"run",fake_run)
    result=Executor(tmp_path).perform(step(tool="android.swipe",x1=1,y1=2,x2=3,y2=4,duration_ms=450),threading.Event())
    assert "OK" in result
    assert commands[-1]==["/adb","-s","ONE","shell","input","swipe","1","2","3","4","450"]


def test_android_keyevent_whitelisted(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    observed=[]
    monkeypatch.setattr(e,"_adb",lambda serial,*args:observed.append(args) or "OK")
    e.perform(step(tool="android.keyevent",key="BACK"),threading.Event())
    assert observed==[("shell","input","keyevent","KEYCODE_BACK")]


def test_android_screenshot_png_bytes(monkeypatch,tmp_path):
    from ai_ai import executor as module
    e=Executor(tmp_path)
    monkeypatch.setattr(e,"_adb_command",lambda serial:["/adb","-s","ONE"])
    data=b"\x89PNG\r\n\x1a\n"+b"test"
    monkeypatch.setattr(module.subprocess,"run",lambda argv,**kw:subprocess.CompletedProcess(argv,0,stdout=data,stderr=b""))
    assert "Captured" in e.perform(step(tool="android.screenshot"),threading.Event())
    assert (tmp_path/"android-screenshot.png").read_bytes()==data


def test_android_screenshot_corrupt_rejected(monkeypatch,tmp_path):
    from ai_ai import executor as module
    e=Executor(tmp_path)
    monkeypatch.setattr(e,"_adb_command",lambda serial:["/adb","-s","ONE"])
    monkeypatch.setattr(module.subprocess,"run",lambda argv,**kw:subprocess.CompletedProcess(argv,0,stdout=b"not png",stderr=b""))
    with pytest.raises(ActionError,match="PNG"):
        e.perform(step(tool="android.screenshot"),threading.Event())
    assert not (tmp_path/"android-screenshot.png").exists()


def test_app_launch_denied_without_allowlist(monkeypatch,tmp_path):
    monkeypatch.delenv("AI_AI_APP_ALLOWLIST_JSON",raising=False)
    with pytest.raises(ActionError,match="not in the owner allowlist"):
        Executor(tmp_path).perform(step(tool="app.launch",alias="editor"),threading.Event())


def test_app_launch_uses_argv_not_shell(monkeypatch,tmp_path):
    from ai_ai import executor as module
    monkeypatch.setenv("AI_AI_APP_ALLOWLIST_JSON",'{"editor":["editor-exe","--safe"]}')
    monkeypatch.setattr(module.shutil,"which",lambda name:"/usr/bin/editor-exe")
    recorded=[]
    monkeypatch.setattr(module.subprocess,"Popen",lambda argv,**kwargs:recorded.append((argv,kwargs)))
    result=Executor(tmp_path).perform(step(tool="app.launch",alias="editor"),threading.Event())
    assert "Launched" in result
    assert recorded[0][0]==["editor-exe","--safe"]
    assert "shell" not in recorded[0][1] or recorded[0][1]["shell"] is False


def test_app_launch_disallows_malformed_config(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    for config in ("not-json",'{"editor":"echo bad"}','{"editor":[]}', '{"editor":["ok",null]}'):
        monkeypatch.setenv("AI_AI_APP_ALLOWLIST_JSON",config)
        with pytest.raises(ActionError):
            e.perform(step(tool="app.launch",alias="editor"),threading.Event())


def test_stop_during_action_returns_stopped(tmp_path):
    class FakeExecutor(Executor):
        def perform(self,step,cancel): return "unused"
    executor=FakeExecutor(tmp_path)
    app=make_app(tmp_path,executor=executor)
    def cancelled_action(step,cancel):
        cancel.set()
        raise ActionError("Stopped by user")
    executor.perform=cancelled_action
    c=TestClient(app)
    h={"X-AI-AI-TOKEN":c.get("/api/session").json()["token"]}
    plan=c.post("/api/plan",headers=h,json={"text":"screenshot"}).json()
    out=c.post("/api/execute",headers=h,json={"plan_id":plan["id"],"approval":"I_APPROVE_THIS_PLAN"})
    assert out.json()["status"]=="STOPPED"
    events=c.get("/api/history",headers=h).json()["events"]
    assert any(item["event"]=="EXECUTION_STOPPED" for item in events)


def test_desktop_screenshot_replaces_symlink_without_overwriting_target(monkeypatch,tmp_path):
    from unittest.mock import Mock
    from PIL import Image
    outside=tmp_path/"outside.txt"
    outside.write_text("safeguarded")
    screenshot=tmp_path/"screenshot.png"
    try: screenshot.symlink_to(outside)
    except (OSError, NotImplementedError): pytest.skip("Symlinks unavailable")
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:Mock(screenshot=lambda:Image.new("RGB",(20,20),"white"))))
    assert "saved" in Executor(tmp_path).perform(step(tool="desktop.screenshot"),threading.Event())
    assert outside.read_text()=="safeguarded"
    assert screenshot.read_bytes().startswith(b"\x89PNG")
    assert not screenshot.is_symlink()


def test_ocr_lang_rejects_untrusted_config(monkeypatch):
    from ai_ai.vision import read_screen, VisionError
    from unittest.mock import Mock
    monkeypatch.setenv("AI_AI_OCR_LANG","eng;touch /tmp/evil")
    with pytest.raises(VisionError,match="Invalid OCR"):
        read_screen(Mock())


def test_emergency_stop_invalidates_existing_plans(tmp_path):
    c=TestClient(make_app(tmp_path))
    h={"X-AI-AI-TOKEN":c.get("/api/session").json()["token"]}
    pid=c.post("/api/plan",headers=h,json={"text":"screenshot"}).json()["id"]
    stopped=c.post("/api/stop",headers=h,json={}).json()
    assert stopped["pending_discarded"]==1
    result=c.post("/api/execute",headers=h,json={"plan_id":pid,"approval":"I_APPROVE_THIS_PLAN"})
    assert result.status_code==409
    assert not (tmp_path/"screenshot.png").exists()
