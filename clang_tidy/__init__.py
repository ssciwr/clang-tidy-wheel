import subprocess
import sys
from pathlib import Path
import functools
from importlib.resources import files
import os


@functools.lru_cache(maxsize=None)
def _get_executable(name:str) -> Path:
    possibles = [
        Path(files("clang_tidy") / f"data/bin/{name}{s}")
        for s in ("", ".exe", ".bin", ".dmg")
    ]
    for exe in possibles:
        if exe.exists():
            if os.environ.get("CLANG_TIDY_WHEEL_VERBOSE", None):
                print(f'Found binary: {exe} ')
            return exe

    raise FileNotFoundError(f"No executable found for {name} at\n{possibles}")

def _run(name, *args):
    command = [_get_executable(name)]
    if args:
        command += list(args)
    else:
        command += sys.argv[1:]
    return subprocess.call(command)

def _run_python(name, *args):
    command = [sys.executable, _get_executable(name)]
    if args:
        command += list(args)
    else:
        command += sys.argv[1:]

    # as MS Windows is not able to run Python scripts directly by name,
    # we have to call the interpreter and pass the script as parameter
    return subprocess.call(command)


def clang_tidy():
    raise SystemExit(_run("clang-tidy"))


