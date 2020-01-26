from denite.base.source import Base
from denite.util import Nvim, UserContext, Candidate

WINDOW_HIGHLIGHT_SYNTAX = [
    {"name": "Prefix", "link": "Constant", "re": r"\d\+: \[.\{-}\] ", "next": "Mark",},
    {"name": "Mark", "link": "PreProc", "re": r"[ $%#] ", "next": "Title"},
    {"name": "Title", "link": "Function", "re": ".*"},
]


class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = "window"
        self.kind = "window"
        self.__candidates: Candidates = []

    def on_init(self, context: UserContext) -> None:
        # TODO: deal with other tabs
        tabnr = self.vim.call("tabpagenr")
        max_winnr = self.vim.call("tabpagewinnr", tabnr, "$")
        current_winnr = self.vim.call("tabpagewinnr", tabnr)
        alt_winnr = self.vim.call("tabpagewinnr", tabnr, "#")

        def bufname(bufnr: int) -> str:
            bufname = self.vim.call("bufname", bufnr)
            return bufname if bufname != "" else "[No Name]"

        bufnames = [bufname(x) for x in self.vim.call("tabpagebuflist", tabnr)]

        def winmark(winnr: int) -> str:
            return (
                "$"
                if winnr == max_winnr
                else "%"
                if winnr == current_winnr
                else "#"
                if winnr == alt_winnr
                else " "
            )

        self.__candidates = [
            {
                "word": bufnames[x],
                "abbr": f"{tabnr}: [{x+1}/{max_winnr}] {winmark(x+1)} {bufnames[x]}",
                "action__tabnr": tabnr,
                "action__winnr": x + 1,
            }
            for x in range(max_winnr)
        ]

    def gather_candidates(self, context: UserContext) -> Candidate:
        return self.__candidates

    def highlight(self) -> None:
        for i, syn in enumerate(WINDOW_HIGHLIGHT_SYNTAX):

            def syn_name(key: str) -> str:
                return "_".join([self.syntax_name, syn[key]])

            containedin = f" containedin={self.syntax_name}" if i == 0 else ""
            nextgroup = f" nextgroup={syn_name('next')}" if "next" in syn else ""
            self.vim.command(
                "syntax match {0} /{1}/ contained{2}{3}".format(
                    syn_name("name"), syn["re"], containedin, nextgroup
                )
            )
            self.vim.command(
                "highlight default link {0} {1}".format(syn_name("name"), syn["link"])
            )
