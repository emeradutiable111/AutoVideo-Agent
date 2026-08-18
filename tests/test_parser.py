from autovideo.parser import ScriptParseError, parse_script


def test_parse_markdown_storyboard():
    project = parse_script("""# Demo\n\n## Scene 1: Intro\n- duration: 2.5s\n- visual: blue room\n- narration: Hello\n\n## Scene 2\nvisual: final card\n""")
    assert project.title == "Demo"
    assert len(project.scenes) == 2
    assert project.scenes[0].duration == 2.5
    assert project.scenes[0].visual == "blue room"
    assert project.scenes[1].narration == ""
    assert project.duration == 5.5


def test_parse_rejects_missing_scenes():
    try:
        parse_script("# no scenes", "input.md")
    except ScriptParseError as exc:
        assert "no scenes" in str(exc)
    else:
        raise AssertionError("expected ScriptParseError")


def test_parse_rejects_invalid_duration():
    try:
        parse_script("## Scene\n- duration: 0", "input.md")
    except ScriptParseError as exc:
        assert "greater than zero" in str(exc)
    else:
        raise AssertionError("expected ScriptParseError")
