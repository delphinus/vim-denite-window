import typing
from denite.util import Nvim, Candidates

WINDOW_HIGHLIGHT_SYNTAX = [
    {"name": "Prefix", "link": "Constant", "re": r"\d\+: \[.\{-}\] ", "next": "Mark",},
    {"name": "Mark", "link": "PreProc", "re": r"[ $%#] ", "next": "Title"},
    {"name": "Title", "link": "Function", "re": ".*"},
]


class Window:
    def __init__(self, vim: Nvim) -> None:
        self.vim = vim

    def get_windows(self, tabnr: int, no_current=False, need_marks=True) -> Candidates:
        max_winnr = self.vim.call("tabpagewinnr", tabnr, "$")
        current_winnr = self.vim.call("tabpagewinnr", tabnr)
        alt_winnr = self.vim.call("tabpagewinnr", tabnr, "#")

        def winmark(winnr: int) -> str:
            return (
                (
                    "$"
                    if winnr == max_winnr
                    else "%"
                    if winnr == current_winnr
                    else "#"
                    if winnr == alt_winnr
                    else " "
                )
                if need_marks
                else " "
            )

        def bufname(bufnr: int) -> str:
            bufname = self.vim.call("bufname", bufnr)
            return bufname if bufname != "" else "[No Name]"

        bufnames = [bufname(x) for x in self.vim.call("tabpagebuflist", tabnr)]

        return [
            {
                "word": bufnames[winnr - 1],
                "abbr": f"{tabnr}: [{winnr}/{max_winnr}] {winmark(winnr)} {bufnames[winnr-1]}",
                "action__tabnr": tabnr,
                "action__winnr": winnr,
            }
            for winnr in range(1, max_winnr + 1)
            if not no_current or winnr != current_winnr
        ]

    def highlight(self, syntax_name: str) -> None:
        for i, syn in enumerate(WINDOW_HIGHLIGHT_SYNTAX):

            def syn_name(key: str) -> str:
                return "_".join([syntax_name, syn[key]])

            containedin = f" containedin={syntax_name}" if i == 0 else ""
            nextgroup = f" nextgroup={syn_name('next')}" if "next" in syn else ""
            self.vim.command(
                "syntax match {0} /{1}/ contained{2}{3}".format(
                    syn_name("name"), syn["re"], containedin, nextgroup
                )
            )
            self.vim.command(
                "highlight default link {0} {1}".format(syn_name("name"), syn["link"])
            )
