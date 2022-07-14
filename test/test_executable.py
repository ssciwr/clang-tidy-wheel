import os
import tempfile

import clang_tidy


def test_executable_file():
    exe = clang_tidy._get_executable("clang-tidy")
    assert os.path.exists(exe), "'clang-tidy' executable is missing"
    assert os.access(exe, os.X_OK), "'clang-tidy'program is not executable"


def test_include_iostream():
    fd, compilation_unit = tempfile.mkstemp(suffix=".cpp")
    os.close(fd)
    with open(compilation_unit, "w") as ostr:
        ostr.write("#include <iostream>\n")
    try:
        assert clang_tidy._run("clang-tidy", compilation_unit) == 0
    finally:
        os.remove(compilation_unit)
