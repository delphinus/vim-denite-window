import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / "rplugin/python3"))

from vim_denite_window.source import Window
from pynvim import Nvim
from typing import List, Any, cast
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def test_get_windows(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    vim.command("split text4")
    w = Window(vim)
    for c in [
        {
            "tabnr": 1,
            "current_tabnr": 1,
            "no_current": False,
            "expected": [
                ["text4", "1: [1/4] % text4", 1, 1,],
                ["text3", "1: [2/4] # text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4] $ text1", 1, 4,],
            ],
        },
        {
            "tabnr": 1,
            "current_tabnr": 2,
            "no_current": False,
            "expected": [
                ["text4", "1: [1/4]   text4", 1, 1,],
                ["text3", "1: [2/4]   text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4]   text1", 1, 4,],
            ],
        },
        {
            "tabnr": 1,
            "current_tabnr": 1,
            "no_current": True,
            "expected": [
                ["text3", "1: [2/4] # text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4] $ text1", 1, 4,],
            ],
        },
        {
            "tabnr": 1,
            "current_tabnr": 2,
            "no_current": True,
            "expected": [
                ["text4", "1: [1/4]   text4", 1, 1,],
                ["text3", "1: [2/4]   text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4]   text1", 1, 4,],
            ],
        },
    ]:
        expected = [
            {"word": x[0], "abbr": x[1], "action__tabnr": x[2], "action__winnr": x[3]}
            for x in cast(List[Any], c["expected"])
        ]
        assert expected == w.get_windows(
            c["tabnr"], c["current_tabnr"], c["no_current"]
        )


def test_get_all_windows(vim: Nvim) -> None:
    vim.command("edit text1")
    vim.command("split text2")
    vim.command("split text3")
    vim.command("split text4")
    vim.command("tabnew")
    vim.command("edit text5")
    vim.command("split text6")
    vim.command("split text7")
    vim.command("split text8")
    vim.command("tabnext")
    w = Window(vim)
    for c in [
        {
            "no_current": False,
            "expected": [
                ["text4", "1: [1/4] % text4", 1, 1,],
                ["text3", "1: [2/4] # text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4] $ text1", 1, 4,],
                ["text8", "2: [1/4]   text8", 2, 1,],
                ["text7", "2: [2/4]   text7", 2, 2,],
                ["text6", "2: [3/4]   text6", 2, 3,],
                ["text5", "2: [4/4]   text5", 2, 4,],
            ],
        },
        {
            "no_current": True,
            "expected": [
                ["text3", "1: [2/4] # text3", 1, 2,],
                ["text2", "1: [3/4]   text2", 1, 3,],
                ["text1", "1: [4/4] $ text1", 1, 4,],
                ["text8", "2: [1/4]   text8", 2, 1,],
                ["text7", "2: [2/4]   text7", 2, 2,],
                ["text6", "2: [3/4]   text6", 2, 3,],
                ["text5", "2: [4/4]   text5", 2, 4,],
            ],
        },
    ]:
        expected = [
            {"word": x[0], "abbr": x[1], "action__tabnr": x[2], "action__winnr": x[3]}
            for x in cast(List[Any], c["expected"])
        ]
        assert expected == w.get_all_windows(c["no_current"])
