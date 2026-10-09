"""Grounding tests: never click when label is absent, duplicated or uncertain."""
from types import SimpleNamespace
from unittest.mock import Mock
import pytest
from ai_ai.vision import TextHit, VisionError, locate_unique, evidence_for_planner, read_screen
from ai_ai.android_ui import locate_android
from ai_ai.executor import Executor
from ai_ai.contracts import ProposedPlan
import threading


def typed(**kw):
    return ProposedPlan.model_validate({"steps":[kw]}).steps[0]


def test_unique_screen_label():
    hits=[TextHit("Open", 100,200,60,20,94)]
    assert locate_unique(hits," OPEN ").center==(130,210)


def test_duplicate_labels_block():
    hits=[TextHit("Save",10,20,30,20,95),TextHit("Save",200,20,30,20,95)]
    with pytest.raises(VisionError,match="ambiguous"):
        locate_unique(hits,"Save")


def test_missing_screen_label_blocks():
    with pytest.raises(VisionError,match="not found"):
        locate_unique([],"Save")


def test_ocr_evidence_does_not_include_huge_payload():
    data=[TextHit("x"*101,1,1,10,10,80),TextHit("Hello",10,20,50,20,91)]
    value=evidence_for_planner(data)
    assert "Hello" in value and "x"*101 not in value


def test_desktop_click_grounded(monkeypatch, tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    monkeypatch.setattr("ai_ai.executor.read_screen",lambda _gui:[TextHit("Save",20,30,40,20,90)])
    e=Executor(tmp_path)
    result=e.perform(typed(tool="desktop.click_text",text="Save"),threading.Event())
    gui.click.assert_called_once_with(40,40)
    assert "OCR confidence" in result


def test_desktop_click_ambiguous_has_zero_side_effects(monkeypatch,tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    monkeypatch.setattr("ai_ai.executor.read_screen", lambda _: [TextHit("Save",0,0,20,20,90),TextHit("Save",300,300,20,20,90)])
    with pytest.raises(VisionError,match="ambiguous"):
        Executor(tmp_path).perform(typed(tool="desktop.click_text",text="Save"),threading.Event())
    gui.click.assert_not_called()


def test_wait_text_observes_again_then_succeeds(monkeypatch, tmp_path):
    calls=[]
    def scan(_):
        calls.append(1)
        return [TextHit("Done",5,5,30,20,90)] if len(calls)==2 else []
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:Mock()))
    monkeypatch.setattr("ai_ai.executor.read_screen",scan)
    assert "Verified" in Executor(tmp_path).perform(typed(tool="desktop.wait_text",text="Done",timeout_seconds=2),threading.Event())
    assert len(calls)==2


def test_wait_text_respects_stop(monkeypatch,tmp_path):
    gui=Mock()
    monkeypatch.setattr(Executor,"gui",staticmethod(lambda:gui))
    monkeypatch.setattr("ai_ai.executor.read_screen",lambda _:[])
    event=threading.Event();event.set()
    with pytest.raises(Exception,match="Stopped"):
        Executor(tmp_path).perform(typed(tool="desktop.wait_text",text="Never"),event)


def test_android_lookup_by_text():
    xml='<hierarchy><node text="Settings" content-desc="" bounds="[100,200][300,260]" /></hierarchy>'
    assert locate_android(xml,"SETTINGS")== (200,230)


def test_android_lookup_by_accessibility_description():
    xml='<hierarchy><node text="" content-desc="Go Back" bounds="[4,8][44,48]" /></hierarchy>'
    assert locate_android(xml,"go back")==(24,28)


def test_android_rejects_ambiguous_and_missing():
    xml='<hierarchy><node text="OK" bounds="[1,1][20,20]"/><node text="OK" bounds="[50,50][60,60]" /></hierarchy>'
    with pytest.raises(VisionError,match="2"):
        locate_android(xml,"OK")
    with pytest.raises(VisionError,match="0"):
        locate_android(xml,"Nope")


def test_android_rejects_entities_and_bad_xml():
    with pytest.raises(VisionError,match="entity"):
        locate_android('<!DOCTYPE x [<!ENTITY e "bad">]><hierarchy/>', "x")
    with pytest.raises(VisionError,match="Invalid"):
        locate_android('<hierarchy>', "x")


def test_android_rejects_broken_bounds():
    xml='<hierarchy><node text="OK" bounds="[40,40][1,1]"/></hierarchy>'
    with pytest.raises(VisionError):locate_android(xml,"OK")


def test_android_xml_tap_is_grounded(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    commands=[]
    monkeypatch.setattr(e,"_android_xml",lambda serial:'<hierarchy><node text="Save" bounds="[50,60][150,100]"/></hierarchy>')
    monkeypatch.setattr(e,"_adb",lambda serial,*cmd,**kw:commands.append(cmd) or "OK")
    result=e.perform(typed(tool="android.tap_text",text="Save"),threading.Event())
    assert commands==[("shell","input","tap","100","80")]
    assert "Tapped" in result


def test_android_assert_not_click(monkeypatch,tmp_path):
    e=Executor(tmp_path)
    monkeypatch.setattr(e,"_android_xml",lambda serial:'<hierarchy><node text="Ready" bounds="[0,0][20,20]"/></hierarchy>')
    fn=Mock();monkeypatch.setattr(e,"_adb",fn)
    assert "Verified" in e.perform(typed(tool="android.assert_text",text="Ready"),threading.Event())
    fn.assert_not_called()


def test_real_tesseract_on_synthetic_screen():
    pytest.importorskip("pytesseract")
    import shutil
    if not shutil.which("tesseract"):
        pytest.skip("Tesseract binary unavailable")
    from PIL import Image, ImageFont, ImageDraw
    image=Image.new("RGB",(500,180),"white")
    font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",48)
    ImageDraw.Draw(image).text((80,40),"SAVE",font=font,fill="black")
    hits=read_screen(SimpleNamespace(screenshot=lambda:image))
    assert locate_unique(hits,"SAVE").confidence>=65
