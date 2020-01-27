import sys
from pathlib import Path

print(str(Path(__file__).parent.parent.parent / "rplugin/python3"))
sys.path.append(str(Path(__file__).parent.parent.parent / "rplugin/python3"))

from vim_denite_window.kind import Window
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_jump(vim):
    vim.command("edit file1.txt")
    vim.command("split file2.txt")
    vim.command("split file3.txt")
    vim.command("tabnew")
    vim.command("edit file4.txt")
    vim.command("split file5.txt")
    vim.command("split file6.txt")
    w = Window(vim)
    w.jump({"action__tabnr": 1, "action__winnr": 3})  # file1.txt
    assert Path(vim.current.buffer.name).name == "file1.txt"
    _close_all(vim, 6)


def test_only(vim):
    vim.command("edit file1.txt")
    vim.command("split file2.txt")
    vim.command("split file3.txt")
    w = Window(vim)
    w.only({"action__tabnr": 1, "action__winnr": 1})  # file3.txt
    assert vim.call("winnr", "$") == 1
    assert Path(vim.current.buffer.name).name == "file3.txt"
    _close_all(vim, 1)


def test_delete(vim):
    vim.command("edit file1.txt")
    vim.command("split file2.txt")
    vim.command("split file3.txt")
    vim.command("tabnew")
    vim.command("edit file4.txt")
    vim.command("split file5.txt")
    vim.command("split file6.txt")
    w = Window(vim)
    w.delete(
        [
            {"action__tabnr": 1, "action__winnr": 1},  # file3.txt
            {"action__tabnr": 1, "action__winnr": 2},  # file2.txt
            {"action__tabnr": 2, "action__winnr": 1},  # file6.txt
            {"action__tabnr": 2, "action__winnr": 2},  # file5.txt
        ]
    )
    assert vim.call("winnr", "$") == 1
    assert Path(vim.tabpages[0].window.buffer.name).name == "file1.txt"
    assert Path(vim.tabpages[1].window.buffer.name).name == "file4.txt"
    _close_all(vim, 2)


def _close_all(vim, num):
    for x in range(num - 1):
        vim.command("close")
    vim.command("enew")
