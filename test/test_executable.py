import os
import sys
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def ensure_tidy_from_wheel(monkeypatch):
    """test the installed clang_tidy package, not the local one"""
    this_dir = Path(__file__).resolve().absolute().parent
    for pd in (this_dir, this_dir / '..'):
        try:
            new_path = sys.path.remove(pd)
            monkeypatch.setattr(sys, "path", new_path)
        except ValueError:
            pass
    monkeypatch.delitem(sys.modules, "clang_tidy", raising=False)

def test_executable_file():
    import clang_tidy
    exe = clang_tidy._get_executable("clang-tidy")
    assert os.path.exists(exe)
    assert os.access(exe, os.X_OK)


def test_include_iostream():
    import clang_tidy
    fd, compilation_unit = tempfile.mkstemp(suffix=".cpp")
    os.close(fd)
    with open(compilation_unit, "w") as ostr:
        ostr.write("#include <iostream>\n")
    try:
        assert clang_tidy._run("clang-tidy", "--extra-arg=-v", compilation_unit) == 0
    finally:
        os.remove(compilation_unit)
