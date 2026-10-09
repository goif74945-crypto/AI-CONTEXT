import pytest
from pydantic import ValidationError
from ai_ai.contracts import ProposedPlan
from ai_ai.planner import parse_rules, PlanningError

@pytest.mark.parametrize("text,expected", [
    ("พิมพ์ สวัสดี", "desktop.type"),
    ("click 500 300", "desktop.click"),
    ("กด ctrl+s", "desktop.hotkey"),
    ("screenshot", "desktop.screenshot"),
    ("เปิด browser", "app.open"),
    ("เขียนไฟล์ test.py :: print(1)", "file.write"),
    ("รันไฟล์ test.py", "code.run"),
    ("มือถือแตะ 12 13", "android.tap"),
    ("มือถือพิมพ์ Hi there", "android.text"),
    ("มือถือเปิด com.android.settings", "android.open"),
])
def test_rule_tools(text, expected):
    p=parse_rules(text)
    assert len(p.steps)==1 and p.steps[0].tool==expected

def test_multistep_order():
    assert [step.tool for step in parse_rules("open notepad\ntype Hello\nhotkey ctrl+s").steps] == ["app.open","desktop.type","desktop.hotkey"]

@pytest.mark.parametrize("text", ["", "delete everything", "กด ctrl+evil", "click -1 0", "มือถือพิมพ์ ;rm -rf", "คลิก 100000 0"])
def test_fail_closed_commands(text):
    with pytest.raises(PlanningError): parse_rules(text)

def test_model_extra_tool_rejected():
    with pytest.raises(ValidationError):
        ProposedPlan.model_validate({"steps":[{"tool":"system.shell", "command":"echo hi"}]})

def test_model_extra_args_rejected():
    with pytest.raises(ValidationError):
        ProposedPlan.model_validate({"steps":[{"tool":"desktop.click", "x":1, "y":2, "command":"x"}]})

def test_max_steps():
    with pytest.raises(PlanningError): parse_rules("screenshot\n"*25)

def test_android_command_injection_rejected():
    for value in ["foo;ls", "Hello$HOME", "who`ami`", "ไทย"]:
        with pytest.raises(ValidationError):
            ProposedPlan.model_validate({"steps":[{"tool":"android.text","text":value}]})

def test_android_package_injection_rejected():
    with pytest.raises(ValidationError):
        ProposedPlan.model_validate({"steps":[{"tool":"android.open","package":"a.b;reboot"}]})
