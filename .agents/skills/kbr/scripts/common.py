"""Shared configuration and local state files for the recall commands."""

import json
import os
import re
import shutil
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile

SKILL_ROOT = Path(__file__).resolve().parents[1]
VAULT_ROOT = SKILL_ROOT.parents[2]
FRONTMATTER = re.compile(r"\A\ufeff*---[ \t]*\r?\n(.*?)(?=^---[ \t]*\r?$)", re.M | re.S)


def load_json(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return default


def load_config():
    config = load_json(SKILL_ROOT / "config.json")
    config.update(load_json(SKILL_ROOT / "config.local.json", {}))
    config["kb_path"] = (VAULT_ROOT / Path(config["kb_path"]).expanduser()).resolve()
    config["state_dir"] = (SKILL_ROOT / Path(config["state_dir"]).expanduser()).resolve()
    return config


@contextmanager
def state_lock(directory):
    """Serialize CLI updates to a state directory. Closing releases the lock."""
    with (directory / "review.lock").open("a+b") as handle:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(handle, fcntl.LOCK_EX)
        yield


def write_text(path, text):
    """Replace a file only after its new contents have been written in full."""
    with NamedTemporaryFile(
        mode="w", encoding="utf-8", newline="", dir=path.parent, delete=False
    ) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(text)
        except BaseException:
            handle.close()
            temporary.unlink()
            raise
    try:
        if path.exists():
            shutil.copymode(path, temporary)
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def save_json(path, data):
    write_text(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def load_index(config):
    index = load_json(config["state_dir"] / "index.json")
    if index is None:
        raise SystemExit("Run index_kb.py to build the recall index first.")
    if Path(index["kb_root"]) != config["kb_path"]:
        raise SystemExit("The wiki path changed. Run index_kb.py to rebuild the recall index.")
    return index
