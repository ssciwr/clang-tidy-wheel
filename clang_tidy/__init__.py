import os
import subprocess
import sys


def _get_executable(name):
    return os.path.join(os.path.dirname(__file__), "data", "bin", name)

def _run(name):
    executable = _get_executable(name)
    return subprocess.call([executable] + sys.argv[1:])

def _run_python(name):
    script = _get_executable(name)
    # as MS Windows is not able to run Python scripts directly by name,
    # we have to call the interpreter and pass the script as parameter
    return subprocess.call([sys.executable, script] + sys.argv[1:])


def clang_tidy():
    raise SystemExit(_run("clang-tidy"))


