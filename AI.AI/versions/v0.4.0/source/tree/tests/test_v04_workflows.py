"""v0.4 real-regression tests: conditional waits, integrity, stop race, stale UI and request policy."""
from __future__ import annotations

import hashlib
import threading
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from ai_ai.browser import BrowserAdapter, BrowserError
from ai_ai.contracts import PlanRequest, ProposedPlan
from ai_ai.executor import ActionError, Executor
from ai_ai.planner import PlanningError, parse_rules, validate_user_grounding
from ai_ai.server import Runtime, make_app
from ai_ai.vision import TextHit


def typed(**kw):
    return ProposedPlan.model_validate({"steps": [kw]}).steps[0]


@pytest.mark.parametrize("command,tool", [
    ("รอหน้าต่าง VS Code :: 8", "desktop.wait_window"),
    ("wait window TextEdit :: 4", "desktop.wait_window"),
    ("browser wait role button :: Submit :: 3", "browser.wait_role"),
    ("เว็บรอบทบาท link :: Help :: 5", "browser.wait_role"),
    ("เว็บตรวจค่า Search :: hello world", "browser.assert_value"),
    ("browser assert value Search :: ", "browser.assert_value"),
    ("มือถือรอข้อความ Done :: 8", "android.wait_text"),
    ("android wait text OK :: 6", "android.wait_text"),
    ("assert sha256 notes.txt :: " + "a"*64, "file.assert_sha256"),
    ("ตรวจแฮช notes.txt :: " + "a"*64, "file.assert_sha256"),
])
def test_v04_grammar(command, tool):
    assert parse_rules(command).steps[0].tool == tool


@pytest.mark.parametrize("spec", [
    {"tool": "desktop.wait_window", "title": "OK", "timeout_seconds": 0},
    {"tool": "android.wait_text", "text": "OK", "timeout_seconds": 19},
    {"tool": "browser.wait_role", "role": "shell", "name": "Run"},
    {"tool": "browser.assert_value", "label": "", "text": "hello"},
    {"tool": "file.assert_sha256", "path": "x.txt", "sha256": "not-a-sha"},
    {"tool": "file.assert_sha256", "path": "x.txt", "sha256": "F"*64},
])
def test_v04_contract_rejects_invalid(spec):
    with pytest.raises(ValidationError):
        typed(**spec)


def test_digest_grounding_rejects_invented_value():
    plan=ProposedPlan(steps=[typed(tool="file.assert_sha256", path="notes.txt", sha256="a"*64)])
    with pytest.raises(PlanningError, match="invented a file digest"):
        validate_user_grounding(plan,"ตรวจแฮช notes.txt")


def test_file_hash_success_and_mismatch(tmp_path):
    e=Executor(tmp_path)
    (tmp_path/"hello.txt").write_text("hello", encoding="utf-8")
    digest=hashlib.sha256(b"hello").hexdigest()
    assert "Verified" in e.perform(typed(tool="file.assert_sha256",path="hello.txt",sha256=digest),threading.Event())
    with pytest.raises(ActionError,match="does not match"):
        e.perform(typed(tool="file.assert_sha256",path="hello.txt",sha256="0"*64),threading.Event())


def test_hash_denies_escape_and_big_file(tmp_path):
    e=Executor(tmp_path)
    with pytest.raises(ActionError,match="workspace"):
        e.perform(typed(tool="file.assert_sha256",path="../secret.txt",sha256="0"*64),threading.Event())
    (tmp_path/"huge.bin").write_bytes(b"0"*5_000_001)
    with pytest.raises(ActionError,match="5 MB"):
        e.perform(typed(tool="file.assert_sha256",path="huge.bin",sha256="0"*64),threading.Event())


def test_desktop_wait_window_becomes_ready(monkeypatch,tmp_path):
    gui=Mock()
    gui.getActiveWindow.return_value.title="Wrong"
    calls=0
    def getter():
        nonlocal calls
        calls+=1
        window=Mock()
        window.title="Editor" if calls>=2 else "Other"
        return window
    gui.getActiveWindow.side_effect=getter
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    result=Executor(tmp_path).perform(typed(tool="desktop.wait_window", title="Editor", timeout_seconds=2),threading.Event())
    assert "Verified" in result and calls==2


def test_desktop_wait_window_unsupported_raises_immediately(monkeypatch,tmp_path):
    gui=Mock(spec=["click"])
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    with pytest.raises(ActionError,match="unavailable"):
        Executor(tmp_path).perform(typed(tool="desktop.wait_window",title="Editor"),threading.Event())


def test_android_wait_text_observes_change(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    xmls=iter(['<hierarchy/>','<hierarchy><node text="OK" bounds="[0,0][10,10]"/></hierarchy>'])
    monkeypatch.setattr(e,"_android_xml",lambda s:next(xmls))
    assert "Verified" in e.perform(typed(tool="android.wait_text",text="OK", timeout_seconds=2),threading.Event())


def test_android_wait_text_stop_before_adb(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    fn=Mock()
    monkeypatch.setattr(e,"_android_xml",fn)
    event=threading.Event();event.set()
    with pytest.raises(ActionError,match="Stopped"):
        e.perform(typed(tool="android.wait_text",text="OK"),event)
    fn.assert_not_called()


def test_desktop_stale_ocr_coordinate_rejected(monkeypatch,tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    scans=iter([[TextHit("Save",10,10,40,20,98)], [TextHit("Save",200,10,40,20,98)]])
    monkeypatch.setattr("ai_ai.executor.read_screen",lambda _:next(scans))
    with pytest.raises(ActionError,match="moved"):
        Executor(tmp_path).perform(typed(tool="desktop.click_text",text="Save"),threading.Event())
    gui.click.assert_not_called()


def test_desktop_ocr_stop_after_scanning(monkeypatch,tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    event=threading.Event()
    def scan(_):
        event.set()
        return [TextHit("Save",10,10,40,20,98)]
    monkeypatch.setattr("ai_ai.executor.read_screen",scan)
    with pytest.raises(ActionError,match="Stopped"):
        Executor(tmp_path).perform(typed(tool="desktop.click_text",text="Save"),event)
    gui.click.assert_not_called()


def test_android_stale_hierarchy_rejected(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    xs=iter(['<hierarchy><node text="Save" bounds="[10,10][60,60]"/></hierarchy>',
             '<hierarchy><node text="Save" bounds="[300,300][350,350]"/></hierarchy>'])
    monkeypatch.setattr(e,"_android_xml",lambda s:next(xs))
    adb=Mock()
    monkeypatch.setattr(e,"_adb",adb)
    with pytest.raises(ActionError,match="moved"):
        e.perform(typed(tool="android.tap_text",text="Save"),threading.Event())
    adb.assert_not_called()


def test_android_stop_during_hierarchy_read(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    event=threading.Event()
    counter=0
    def xml(_):
        nonlocal counter
        counter+=1
        if counter==2:event.set()
        return '<hierarchy><node text="Save" bounds="[10,10][60,60]"/></hierarchy>'
    monkeypatch.setattr(e,"_android_xml",xml)
    adb=Mock(); monkeypatch.setattr(e,"_adb",adb)
    with pytest.raises(ActionError,match="Stopped"):
        e.perform(typed(tool="android.tap_text",text="Save"),event)
    adb.assert_not_called()


def fake_browser(tmp_path):
    b=BrowserAdapter(tmp_path)
    page=Mock()
    page.url="https://safe.example/ok"
    b._get_page=lambda:page
    b.approved_origin=b._origin(page.url)
    return b,page


def test_browser_wait_role_checks_unique_enabled_and_visible(tmp_path):
    b,page=fake_browser(tmp_path)
    try:
        locator=page.get_by_role.return_value
        locator.count.return_value=1
        assert "Observed" in b.act(typed(tool="browser.wait_role",role="button",name="Next",timeout_seconds=3))
        page.get_by_role.assert_called_once_with("button",name="Next",exact=True)
        locator.first.wait_for.assert_called_once_with(state="visible",timeout=3000)
        locator.is_enabled.return_value=False
        with pytest.raises(BrowserError,match="disabled"):
            b.act(typed(tool="browser.wait_role",role="button",name="Next"))
    finally:b.close()


def test_browser_wait_role_rejects_ambiguity(tmp_path):
    b,page=fake_browser(tmp_path)
    try:
        page.get_by_role.return_value.count.return_value=2
        with pytest.raises(BrowserError,match="found 2"):
            b.act(typed(tool="browser.wait_role",role="button",name="Next"))
    finally:b.close()


def test_browser_assert_value_no_content_leak(tmp_path):
    b,page=fake_browser(tmp_path)
    try:
        loc=page.get_by_label.return_value
        loc.count.return_value=1
        loc.input_value.return_value="super-secret"
        result=b.act(typed(tool="browser.assert_value",label="Password",text="super-secret"))
        assert "Verified" in result and "super-secret" not in result
        loc.input_value.return_value="wrong"
        with pytest.raises(BrowserError,match="does not match"):
            b.act(typed(tool="browser.assert_value",label="Password",text="super-secret"))
    finally:b.close()


def test_browser_request_route_allows_only_approved_origin(tmp_path):
    b=BrowserAdapter(tmp_path)
    try:
        r=Mock();r.request.url="https://safe.example/api"
        b._route_within_origin(r)
        r.abort.assert_called_once_with("blockedbyclient")
        r=Mock();r.request.url="https://safe.example/api"
        b.approved_origin=b._origin("https://safe.example")
        b._route_within_origin(r)
        r.continue_.assert_called_once_with()
        r.abort.assert_not_called()
        for url in ("https://other.example/", "javascript:alert(1)", "https://safe.example.evil.test/", "http://safe.example/"):
            blocked=Mock();blocked.request.url=url
            b._route_within_origin(blocked)
            blocked.abort.assert_called_once_with("blockedbyclient")
            blocked.continue_.assert_not_called()
    finally:b.close()


def test_browser_open_arms_origin_before_navigation(tmp_path):
    b,page=fake_browser(tmp_path)
    b.approved_origin=None
    def navigation(*a,**kw):
        assert b.approved_origin==("https","safe.example",443)
        response=Mock();response.status=200
        return response
    page.goto.side_effect=navigation
    try:
        assert "Opened" in b.act(typed(tool="browser.open",url="https://safe.example/start"))
        page.goto.side_effect=OSError("network blocked")
        with pytest.raises(BrowserError):
            b.act(typed(tool="browser.open",url="https://safe.example/broken"))
        assert b.approved_origin is None
    finally:b.close()


def test_stop_invalidates_inflight_plan_and_preserves_empty_pending(monkeypatch,tmp_path):
    from ai_ai import server
    runtime=Runtime(tmp_path)
    inside=threading.Event();release=threading.Event()
    original=server.parse_rules
    def slow(text):
        inside.set()
        assert release.wait(3)
        return original(text)
    monkeypatch.setattr(server,"parse_rules",slow)
    outcome=[]
    worker=threading.Thread(target=lambda: _store_outcome(runtime,outcome),daemon=True)
    worker.start()
    assert inside.wait(2)
    with runtime.control_lock:
        runtime.stop_generation+=1
        runtime.cancel.set()
        with runtime.pending_lock:
            runtime.pending.clear()
    release.set();worker.join(3)
    assert not worker.is_alive()
    assert len(outcome)==1 and isinstance(outcome[0],PlanningError)
    assert not runtime.pending


def _store_outcome(runtime,outcome):
    try:outcome.append(runtime.add(PlanRequest(text="screenshot")))
    except Exception as exc:outcome.append(exc)


def test_integration_api_new_wait_and_hash_command(tmp_path):
    class RecordingExecutor(Executor):
        def perform(self,step,cancel):
            return step.tool
    c=TestClient(make_app(tmp_path,executor=RecordingExecutor(tmp_path)))
    token=c.get("/api/session").json()["token"]
    h={"X-AI-AI-TOKEN":token}
    r=c.post("/api/plan",headers=h,json={"text":"browser open https://safe.example\nbrowser wait role button :: Start :: 5\nandroid wait text Ready :: 5"})
    assert r.status_code==200
    view=r.json()
    assert [s["tool"] for s in view["steps"]]==["browser.open", "browser.wait_role", "android.wait_text"]
    assert view["clap_eligible"] is False
    executed=c.post("/api/execute",headers=h,json={"plan_id":view["id"],"approval":"I_APPROVE_THIS_PLAN"})
    assert executed.json()["status"]=="PASS"


def test_assurance_rejects_browser_without_newly_approved_url():
    from ai_ai.assurance import analyze_plan, PlanScopeError
    with pytest.raises(PlanScopeError,match="browser.open"):
        analyze_plan([typed(tool="browser.click_role",role="button",name="Pay")])
    assert analyze_plan([
        typed(tool="browser.open",url="https://safe.example"),
        typed(tool="browser.assert_text",text="Done")
    ])==[]


def test_assurance_rejects_cross_plan_browser_inherited_origin(tmp_path):
    c=TestClient(make_app(tmp_path))
    h={"X-AI-AI-TOKEN":c.get("/api/session").json()["token"]}
    r=c.post("/api/plan",headers=h,json={"text":"browser click role button :: Pay"})
    assert r.status_code==422
    assert "browser.open" in r.json()["detail"]


def test_assurance_warning_is_visible_to_operator(tmp_path):
    c=TestClient(make_app(tmp_path))
    h={"X-AI-AI-TOKEN":c.get("/api/session").json()["token"]}
    p=c.post("/api/plan",headers=h,json={"text":"click 4 5"}).json()
    assert any("coordinate-based" in s for s in p["warnings"])
    assert any("no active-window" in s for s in p["warnings"])
    assert any("no explicit later desktop verification" in s for s in p["warnings"])


def test_assurance_recognizes_explicit_postcondition():
    from ai_ai.assurance import analyze_plan
    warnings=analyze_plan([typed(tool="desktop.type",text="hello",window_title="Editor"),
                           typed(tool="desktop.assert_text",text="hello")])
    assert warnings==[]


@pytest.mark.parametrize("command,expected",[
    ("desktop inspect text", "desktop.inspect_text"),
    ("สำรวจข้อความหน้าจอ", "desktop.inspect_text"),
    ("browser inspect controls", "browser.inspect_controls"),
    ("เว็บสำรวจปุ่ม", "browser.inspect_controls"),
    ("android inspect controls", "android.inspect_controls"),
    ("มือถือสำรวจปุ่ม", "android.inspect_controls"),
    ("browser wait url https://safe.example/done :: 5", "browser.wait_url"),
    ("เว็บรอURL https://safe.example/done :: 5", "browser.wait_url"),
])
def test_inspection_parser(command,expected):
    assert parse_rules(command).steps[0].tool==expected


def test_android_inspection_password_redaction_and_limit():
    from ai_ai.android_ui import inspect_android_controls
    xml='<hierarchy><node text="password1" password="true" bounds="[0,0][8,8]"/>'
    xml += '<node text="hidden" visible-to-user="false" bounds="[0,0][8,8]"/>'
    xml += ''.join(f'<node text="Item{i}" bounds="[1,1][20,20]" />' for i in range(60))
    controls=inspect_android_controls(xml+'</hierarchy>')
    assert len(controls)==40
    assert all(c['label'].startswith('Item') for c in controls)
    assert 'password1' not in str(controls)


@pytest.mark.parametrize('xml',["<!DOCTYPE x><hierarchy/>", '<hierarchy>', '<!ENTITY x "a"><hierarchy/>'])
def test_android_inspection_malformed_xml_rejected(xml):
    from ai_ai.android_ui import inspect_android_controls
    from ai_ai.vision import VisionError
    with pytest.raises(VisionError):inspect_android_controls(xml)


def test_android_inspection_no_tap(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    monkeypatch.setattr(e,'_android_xml',lambda serial:'<hierarchy><node text="Save" bounds="[0,0][50,50]"/></hierarchy>')
    adb=Mock(); monkeypatch.setattr(e,'_adb',adb)
    result=e.perform(typed(tool='android.inspect_controls'),threading.Event())
    assert 'Save' in result
    adb.assert_not_called()


def test_desktop_inspection_never_clicks(monkeypatch,tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,'gui',staticmethod(lambda:gui))
    monkeypatch.setattr('ai_ai.executor.read_screen',lambda _: [TextHit('Ready',2,4,40,20,95)])
    output=Executor(tmp_path).perform(typed(tool='desktop.inspect_text'),threading.Event())
    assert 'Ready' in output
    gui.click.assert_not_called()
    gui.hotkey.assert_not_called()


def test_browser_inspection_does_not_invoke_click_or_form_fill(tmp_path):
    b,p=fake_browser(tmp_path)
    try:
        p.locator.return_value.evaluate_all.return_value=[{'role':'button','name':'Save','enabled':True}]
        assert 'Save' in b.act(typed(tool='browser.inspect_controls'))
        p.get_by_role.assert_not_called()
        p.get_by_label.assert_not_called()
    finally:b.close()


def test_browser_wait_url_requires_approved_origin(tmp_path):
    b,p=fake_browser(tmp_path)
    try:
        with pytest.raises(BrowserError,match='unapproved'):
            b.act(typed(tool='browser.wait_url',url='https://evil.example/',timeout_seconds=3))
        p.wait_for_url.assert_not_called()
        assert 'Observed' in b.act(typed(tool='browser.wait_url',url='https://safe.example/ok'))
    finally:b.close()


def test_browser_inspect_requires_same_plan_url(tmp_path):
    c=TestClient(make_app(tmp_path))
    h={'X-AI-AI-TOKEN':c.get('/api/session').json()['token']}
    no=c.post('/api/plan',headers=h,json={'text':'เว็บสำรวจปุ่ม'})
    assert no.status_code==422
    yes=c.post('/api/plan',headers=h,json={'text':'เว็บเปิด https://safe.example\nเว็บสำรวจปุ่ม'})
    assert yes.status_code==200
    assert [a['tool'] for a in yes.json()['steps']]==['browser.open','browser.inspect_controls']


def test_stop_during_screen_evidence_prevents_model_call(monkeypatch,tmp_path):
    from ai_ai import server
    inside=threading.Event();release=threading.Event()
    class WaitingOCR(Executor):
        def read_screen_evidence(self):
            inside.set()
            assert release.wait(2)
            return "Sensitive visible text"
    runtime=Runtime(tmp_path,executor=WaitingOCR(tmp_path))
    planner=Mock(side_effect=AssertionError("Must not invoke model after Stop"))
    monkeypatch.setattr(server,'parse_llm',planner)
    outcomes=[]
    def run():
        try:runtime.add(PlanRequest(text='take a screenshot',use_ai=True,share_screen_text=True))
        except Exception as exc:outcomes.append(exc)
    t=threading.Thread(target=run,daemon=True);t.start()
    assert inside.wait(2)
    with runtime.control_lock:
        runtime.stop_generation+=1
        runtime.cancel.set()
    release.set();t.join(3)
    assert len(outcomes)==1 and isinstance(outcomes[0],PlanningError)
    planner.assert_not_called()


def test_audit_failure_does_not_publish_approval_token(monkeypatch,tmp_path):
    runtime=Runtime(tmp_path)
    monkeypatch.setattr(runtime.audit,'record',Mock(side_effect=OSError('audit volume full')))
    with pytest.raises(OSError,match='volume full'):
        runtime.add(PlanRequest(text='screenshot'))
    assert not runtime.pending


@pytest.mark.skipif(__import__('os').name=='nt',reason='POSIX process group signal semantics test')
def test_stop_kills_script_subprocess_in_same_group(tmp_path):
    import time,sys
    e=Executor(tmp_path,enable_code_run=True)
    child=("import time,pathlib;time.sleep(.7);pathlib.Path('child-done').write_text('alive')")
    script=("import subprocess,sys,time,pathlib\n"
            f"subprocess.Popen([sys.executable,'-I','-c',{child!r}])\n"
            "pathlib.Path('child-started').write_text('yes')\n"
            "time.sleep(30)\n")
    (tmp_path/'spawn.py').write_text(script,encoding='utf8')
    cancel=threading.Event();failed=[]
    def run():
        try:e.perform(typed(tool='code.run',path='spawn.py',timeout_seconds=10),cancel)
        except Exception as exc:failed.append(exc)
    thread=threading.Thread(target=run,daemon=True);thread.start()
    deadline=time.monotonic()+4
    while not (tmp_path/'child-started').exists() and time.monotonic()<deadline:
        time.sleep(.025)
    assert (tmp_path/'child-started').exists()
    cancel.set();thread.join(3)
    assert not thread.is_alive()
    assert len(failed)==1 and isinstance(failed[0],ActionError)
    time.sleep(.85)
    assert not (tmp_path/'child-done').exists()
