import os
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def ensure_tidy_from_wheel(monkeypatch):
    """test the installed clang_tidy package, not the local one"""
    this_dir = Path(__file__).resolve().absolute().parent
    for pd in (this_dir, this_dir / ".."):
        try:
            new_path = sys.path.remove(pd)
            monkeypatch.setattr(sys, "path", new_path)
        except ValueError:
            pass
    monkeypatch.delitem(sys.modules, "clang_tidy", raising=False)


def test_executable_file(capsys):
    import clang_tidy

    clang_tidy._get_executable.cache_clear()
    exe = clang_tidy._get_executable("clang-tidy")
    assert os.path.exists(exe)
    assert os.access(exe, os.X_OK)
    assert capsys.readouterr().out == ""


def _test_code(code: str):
    import clang_tidy

    fd, compilation_unit = tempfile.mkstemp(suffix=".cpp")
    os.close(fd)
    with open(compilation_unit, "w") as ostr:
        ostr.write(code)
    try:
        assert clang_tidy._run("clang-tidy", "--extra-arg=-v", compilation_unit) == 0
    finally:
        os.remove(compilation_unit)


def test_verbose_output(capsys, monkeypatch):
    import clang_tidy
    monkeypatch.setenv("CLANG_TIDY_WHEEL_VERBOSE", "1")
    # need to clear cache to make sure the function is run again
    clang_tidy._get_executable.cache_clear()
    clang_tidy._get_executable("clang-tidy")
    assert capsys.readouterr().out


@pytest.mark.skipif(
    os.environ.get("CI", None) and "linux" in sys.platform,
    reason="https://github.com/ssciwr/clang-tidy-wheel/issues/30",
)
def test_include_iostream():
    _test_code("#include <iostream>\n")


def test_main():
    _test_code("int main() { return 0;}\n")
