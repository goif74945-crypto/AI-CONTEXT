import pathlib
import sys
import threading
import pytest
from ai_ai.executor import Executor, ActionError
from ai_ai.contracts import ProposedPlan

def step(**kw):
    return ProposedPlan.model_validate({"steps":[kw]}).steps[0]

def test_workspace_traversal(tmp_path):
    e=Executor(tmp_path / "workspace")
    for path in ["../outside.txt", "/tmp/secret", "C:\\Windows\\win.ini", "folder/../../outside"]:
        with pytest.raises(ActionError): e.safe_path(path)

def test_symlink_escape(tmp_path):
    workspace=tmp_path / "workspace"
    e=Executor(workspace)
    outside=tmp_path / "outside"
    outside.mkdir()
    try:
        (workspace/"link").symlink_to(outside, target_is_directory=True)
    except (OSError,NotImplementedError):
        pytest.skip("symlink unsupported by OS permissions")
    with pytest.raises(ActionError):e.safe_path("link/file.txt")

def test_file_write_read(tmp_path):
    e=Executor(tmp_path)
    assert "Wrote" in e.perform(step(tool="file.write",path="project/demo.py", content="print('hi')"),threading.Event())
    assert e.perform(step(tool="file.read",path="project/demo.py"),threading.Event()) == "print('hi')"

def test_read_oversize_denied(tmp_path):
    e=Executor(tmp_path)
    (tmp_path/"large.txt").write_text("a"*200001)
    with pytest.raises(ActionError):e.perform(step(tool="file.read",path="large.txt"),threading.Event())

def test_code_run_disabled(tmp_path):
    e=Executor(tmp_path)
    (tmp_path/"demo.py").write_text("print(2)")
    with pytest.raises(ActionError,match="disabled"):
        e.perform(step(tool="code.run",path="demo.py"),threading.Event())

def test_code_run_trusted_script(tmp_path):
    e=Executor(tmp_path, enable_code_run=True)
    (tmp_path/"demo.py").write_text("print(2 + 3)",encoding="utf8")
    assert "5" in e.perform(step(tool="code.run",path="demo.py",timeout_seconds=3),threading.Event())

def test_script_failure_stops(tmp_path):
    e=Executor(tmp_path, enable_code_run=True)
    (tmp_path/"bad.py").write_text("raise ValueError('expected')")
    with pytest.raises(ActionError,match="Script exit code"):
        e.perform(step(tool="code.run",path="bad.py"),threading.Event())

def test_code_run_cancellation(tmp_path):
    e=Executor(tmp_path,enable_code_run=True)
    (tmp_path/"demo.py").write_text("print('won\\'t execute')")
    flag=threading.Event();flag.set()
    with pytest.raises(ActionError,match="Stopped"):
        e.perform(step(tool="code.run",path="demo.py"),flag)

def test_code_run_timeout(tmp_path):
    e=Executor(tmp_path,enable_code_run=True)
    (tmp_path/"loop.py").write_text("import time\ntime.sleep(6)")
    with pytest.raises(ActionError,match="timed out"):
        e.perform(step(tool="code.run",path="loop.py",timeout_seconds=1),threading.Event())

def test_android_tap_uses_device_selector_not_shell(monkeypatch,tmp_path):
    import subprocess
    from ai_ai import executor as executor_module
    commands=[]
    monkeypatch.setattr(executor_module.shutil,"which",lambda name:"/mock/adb")
    def fake_run(argv,**kwargs):
        commands.append(argv)
        if argv[-1]=="devices":
            return subprocess.CompletedProcess(argv,0,stdout="List of devices attached\nserial-1\tdevice\n",stderr="")
        return subprocess.CompletedProcess(argv,0,stdout="OK",stderr="")
    monkeypatch.setattr(executor_module.subprocess,"run",fake_run)
    e=Executor(tmp_path)
    result=e.perform(step(tool="android.tap",x=20,y=30),threading.Event())
    assert result=="OK"
    assert commands[-1]==["/mock/adb","-s","serial-1","shell","input","tap","20","30"]

def test_android_requires_authorized_unique_device(monkeypatch,tmp_path):
    import subprocess
    from ai_ai import executor as executor_module
    monkeypatch.setattr(executor_module.shutil,"which",lambda name:"/mock/adb")
    def fake_run(argv,**kwargs):
        return subprocess.CompletedProcess(argv,0,stdout="List of devices attached\nA\tdevice\nB\tdevice\n",stderr="")
    monkeypatch.setattr(executor_module.subprocess,"run",fake_run)
    e=Executor(tmp_path)
    with pytest.raises(ActionError,match="exactly one"):
        e.perform(step(tool="android.tap",x=20,y=30),threading.Event())
