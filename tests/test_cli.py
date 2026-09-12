from main import main


def test_cli_register_and_whoami(tmp_path, monkeypatch, capsys):
    users_path = tmp_path / "users.json"
    users_path.write_text("[]")
    monkeypatch.setattr("main.default_auth_manager.users_store.filename", str(users_path))
    monkeypatch.setattr("main.default_auth_manager.session_path", tmp_path / "session.json")
    monkeypatch.setattr("getpass.getpass", lambda prompt: "hunter2")

    assert main(["register", "neo"]) == 0
    assert main(["login", "neo"]) == 0
    assert main(["whoami"]) == 0
    assert "neo (user)" in capsys.readouterr().out


def test_cli_admin_status_requires_admin(tmp_path, monkeypatch, capsys):
    users_path = tmp_path / "users.json"
    users_path.write_text("[]")
    monkeypatch.setattr("main.default_auth_manager.users_store.filename", str(users_path))
    monkeypatch.setattr("main.default_auth_manager.session_path", tmp_path / "session.json")
    monkeypatch.setattr("getpass.getpass", lambda prompt: "hunter2")

    main(["register", "neo"])
    main(["login", "neo"])
    assert main(["admin-status"]) == 0
    assert "permission" in capsys.readouterr().out