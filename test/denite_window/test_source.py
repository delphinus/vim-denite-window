import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent / "rplugin/python3"))

from vim_denite_window.source import Window
from pynvim import Nvim
from typing import Any, Dict, List, cast
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


def test_highlight(vim: Nvim) -> None:
    # vim.current.buffer.add_highlight("Test", 0)
    vim.command("syntax match Test /.*/")
    vim.command("highlight default link Test Statement")
    w = Window(vim)
    w.highlight("Test")
    logger.info(vim.command_output("syn"))
    for c in [
        {"line": "12: [34/56] % text1", "expected": ["12: [34/56] ", "% ", "text1"],},
    ]:
        vim.command("enew!")
        vim.current.buffer[0] = c["line"]
        logger.info(vim.command_output("echo synID(1, 1, 0)"))
        assert getSyntaxChars(vim) == [
            {"name": "Test_Prefix", "chars": c["expected"][0]},
            {"name": "Test_Mark", "chars": c["expected"][1]},
            {"name": "Test_Title", "chars": c["expected"][2]},
        ]


def getSyntaxChars(vim: Nvim) -> List[Dict[str, str]]:
    def synName(col: int) -> str:
        synId: int = vim.call("synID", 1, col + 1, True)
        syn: int = vim.call("synIDtrans", synId)
        logger.info([col + 1, synId, syn, vim.call("synIDattr", syn, "name")])
        return cast(str, vim.call("synIDattr", syn, "name"))

    name = synName(0)
    line: str = vim.current.buffer[0]
    logger.info(line)
    chars: List[Dict[str, str]] = []

    for c, char in enumerate(line):
        if c == 0:
            chars = [{"name": name, "chars": char}]
        else:
            n = synName(c)
            if n == name:
                chars[-1]["chars"] += char
            else:
                chars += [{"name": n, "chars": char}]
                name = n

    return chars
