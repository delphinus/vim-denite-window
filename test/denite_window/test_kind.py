import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / "rplugin/python3"))

from vim_denite_window.kind import Window
from pynvim import Nvim
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_open(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    w = Window(vim)
    w.open({"action__tabnr": 1, "action__winnr": 3})  # text1
    assert [Path(x.buffer.name).name for x in vim.windows] == [
        "text1",
        "text2",
        "text1",
    ]


def test_jump(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    vim.command("tabnew")
    vim.command("edit text4")
    vim.command("split text5")
    vim.command("split text6")
    w = Window(vim)
    w.jump({"action__tabnr": 1, "action__winnr": 3})  # text1
    assert Path(vim.current.buffer.name).name == "text1"


def test_only(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    w = Window(vim)
    w.only({"action__tabnr": 1, "action__winnr": 1})  # text3
    assert vim.funcs.winnr("$") == 1
    assert Path(vim.current.buffer.name).name == "text3"


def test_delete(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    vim.command("tabnew")
    vim.command("edit text4")
    vim.command("split text5")
    vim.command("split text6")
    w = Window(vim)
    w.delete(
        [
            {"action__tabnr": 1, "action__winnr": 1},  # text3
            {"action__tabnr": 1, "action__winnr": 2},  # text2
            {"action__tabnr": 2, "action__winnr": 1},  # text6
            {"action__tabnr": 2, "action__winnr": 2},  # text5
        ]
    )
    assert vim.funcs.winnr("$") == 1
    assert Path(vim.tabpages[0].window.buffer.name).name == "text1"
    assert Path(vim.tabpages[1].window.buffer.name).name == "text4"
