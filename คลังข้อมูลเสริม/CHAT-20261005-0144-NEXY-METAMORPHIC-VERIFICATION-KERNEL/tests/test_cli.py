import json

from nexy_mvk.cli import main


def test_validate_fixture_cli(tmp_path, capsys):
    fixture = tmp_path / "fixture.json"
    fixture.write_text(json.dumps({
        "case": {"prompt": "x", "permissions": ["read"]},
        "observation": {"status": "PASS", "released": True, "payload": {"ok": True}},
    }), encoding="utf-8")
    assert main(["validate-fixture", str(fixture)]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "PASS"
    assert len(output["case_hash"]) == 64


def test_validate_fixture_cli_fails_closed(tmp_path, capsys):
    fixture = tmp_path / "bad.json"
    fixture.write_text("{}", encoding="utf-8")
    assert main(["validate-fixture", str(fixture)]) == 2
    assert "missing fixture keys" in capsys.readouterr().err
