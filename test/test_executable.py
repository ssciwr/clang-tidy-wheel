import os
import sys
import tempfile

import pytest


@pytest.fixture(autouse=True, scope='session')
def avoid_local_import(monkeypatch):
    """all test functions automatically load this fixture"""
    # test the installed clang_tidy package, not the local one
    monkeypatch.delitem(sys.path, os.path.dirname(os.path.dirname(__file__)))


def test_executable_file():
    import clang_tidy

    exe = clang_tidy._get_executable("clang-tidy")
    assert os.path.exists(exe), "'clang-tidy' executable is missing"
    assert os.access(exe, os.X_OK), "'clang-tidy'program is not executable"


def test_include_iostream():
    if os.environ.get("RUNNER_OS", "None").lower() == "macos":
        pytest.xfail("https://github.com/ssciwr/clang-tidy-wheel/issues/19")
    import clang_tidy

    fd, compilation_unit = tempfile.mkstemp(suffix=".cpp")
    os.close(fd)
    with open(compilation_unit, "w") as ostr:
        ostr.write("#include <iostream>\n")
    try:
        assert clang_tidy._run("clang-tidy", "--extra-arg=-v", compilation_unit) == 0
    finally:
        os.remove(compilation_unit)
