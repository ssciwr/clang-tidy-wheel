import subprocess
import sys

import pkg_resources


def _get_executable(name):
    return pkg_resources.resource_filename('clang_tidy', f"data/bin/{name}")

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


