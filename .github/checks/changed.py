"""Файлы, изменённые в этом PR: git diff base...head (только имена)."""
import os
import subprocess


def changed_files():
    base = os.environ["BASE_SHA"]
    out = subprocess.run(["git", "diff", "--name-only", base, "HEAD"], capture_output=True, text=True, check=True)
    return [f for f in out.stdout.split("\n") if f and not f.startswith(".github/")]


def added_lines(path):
    base = os.environ["BASE_SHA"]
    out = subprocess.run(["git", "diff", "-U0", base, "HEAD", "--", path], capture_output=True, text=True, check=True)
    return [l[1:] for l in out.stdout.split("\n") if l.startswith("+") and not l.startswith("+++")]


def at_base(path):
    base = os.environ["BASE_SHA"]
    out = subprocess.run(["git", "show", f"{base}:{path}"], capture_output=True, text=True)
    return out.stdout if out.returncode == 0 else ""
