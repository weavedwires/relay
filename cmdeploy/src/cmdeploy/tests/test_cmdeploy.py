import importlib
import os
from types import SimpleNamespace

import pytest

from cmdeploy.cmdeploy import (
    build_pyinfra_command,
    get_parser,
    get_ssh_target,
    main,
)
from cmdeploy.www import get_paths


@pytest.fixture(autouse=True)
def _chdir(tmp_path):
    old = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(old)


class TestCmdline:
    def test_parser(self, capsys):
        parser = get_parser()
        parser.parse_args([])
        init = parser.parse_args(["init", "chat.example.org"])
        run = parser.parse_args(["run"])
        assert init and run

    def test_init_not_overwrite(self, capsys, tmp_path, monkeypatch):
        monkeypatch.delenv("CHATMAIL_INI", raising=False)
        inipath = tmp_path / "chatmail.ini"
        args = ["init", "--config", str(inipath), "chat.example.org"]
        assert main(args) == 0
        capsys.readouterr()

        assert main(args) == 1
        out, err = capsys.readouterr()
        assert "path exists" in out.lower()

        args.insert(1, "--force")
        assert main(args) == 0
        out, err = capsys.readouterr()
        assert "deleting config file" in out.lower()

    def test_dns_skip_on_ip(self, capsys, tmp_path, monkeypatch):
        monkeypatch.delenv("CHATMAIL_INI", raising=False)
        inipath = tmp_path / "chatmail.ini"
        assert main(["init", "--config", str(inipath), "1.3.3.7"]) == 0
        assert main(["dns", "--config", str(inipath)]) == 0
        out, err = capsys.readouterr()
        assert out == "[WARNING] 1.3.3.7 is not a domain, skipping DNS checks.\n"


def test_get_ssh_target():
    config = SimpleNamespace(ssh_user="root")
    assert get_ssh_target("chat.example.org", config) == ("chat.example.org", "root")
    assert get_ssh_target("deploy@chat.example.org", config) == (
        "chat.example.org",
        "deploy",
    )
    assert get_ssh_target("localhost", config) == ("localhost", "root")

    config.ssh_user = "deploy"
    assert get_ssh_target("chat.example.org", config) == ("chat.example.org", "deploy")


def test_build_pyinfra_command(monkeypatch):
    deploy_path = "/tmp/run.py"
    assert (
        build_pyinfra_command("pyinfra", "chat.example.org", "root", deploy_path)
        == "pyinfra --ssh-user root chat.example.org /tmp/run.py -y"
    )
    assert (
        build_pyinfra_command("pyinfra", "chat.example.org", "deploy", deploy_path)
        == "pyinfra --ssh-user deploy --sudo chat.example.org /tmp/run.py -y"
    )

    monkeypatch.setattr("cmdeploy.cmdeploy.os.geteuid", lambda: 1000)
    assert (
        build_pyinfra_command("pyinfra", "localhost", "root", deploy_path)
        == "pyinfra --sudo @local /tmp/run.py -y"
    )

    monkeypatch.setattr("cmdeploy.cmdeploy.os.geteuid", lambda: 0)
    assert (
        build_pyinfra_command("pyinfra", "localhost", "deploy", deploy_path)
        == "pyinfra @local /tmp/run.py -y"
    )


def test_www_folder(example_config, tmp_path):
    reporoot = importlib.resources.files(__package__).joinpath("../../../../").resolve()
    assert not example_config.www_folder
    www_path, src_dir, build_dir = get_paths(example_config)
    assert www_path.absolute() == reporoot.joinpath("www").absolute()
    assert src_dir == reporoot.joinpath("www").joinpath("src")
    assert build_dir == reporoot.joinpath("www").joinpath("build")
    example_config.www_folder = "disabled"
    www_path, _, _ = get_paths(example_config)
    assert not www_path.is_dir()
    example_config.www_folder = str(tmp_path)
    www_path, src_dir, build_dir = get_paths(example_config)
    assert www_path == tmp_path
    assert not src_dir.exists()
    assert not build_dir
    src_path = tmp_path.joinpath("src")
    os.mkdir(src_path)
    with open(src_path / "index.md", "w") as f:
        f.write("# Test")
    www_path, src_dir, build_dir = get_paths(example_config)
    assert www_path == tmp_path
    assert src_dir == src_path
    assert build_dir == tmp_path.joinpath("build")
