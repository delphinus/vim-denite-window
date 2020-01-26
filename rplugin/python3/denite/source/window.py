import typing
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
        self.__candidates: Candidates = []
        current_tabnr = self.vim.call("tabpagenr")
        options = self._options(context)
        if options["all"]:
            max_tabnr = self.vim.call("tabpagenr", "$")
            for tabnr in range(1, max_tabnr + 1):
                need_marks = tabnr == current_tabnr
                no_current = need_marks and options["no-current"]
                self._get_windows(tabnr, no_current, need_marks)
        else:
            self._get_windows(current_tabnr, options["no-current"], True)

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

    def _options(self, context: UserContext) -> typing.Dict[str, bool]:
        return {
            "no-current": "no-current" in context["args"],
            "all": "all" in context["args"],
        }

    def _get_windows(self, tabnr: int, no_current: bool, need_marks: bool) -> None:
        max_winnr = self.vim.call("tabpagewinnr", tabnr, "$")
        current_winnr = self.vim.call("tabpagewinnr", tabnr)
        alt_winnr = self.vim.call("tabpagewinnr", tabnr, "#")

        def bufname(bufnr: int) -> str:
            bufname = self.vim.call("bufname", bufnr)
            return bufname if bufname != "" else "[No Name]"

        bufnames = [bufname(x) for x in self.vim.call("tabpagebuflist", tabnr)]

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

        for winnr in range(1, max_winnr + 1):
            if no_current and winnr == current_winnr:
                continue
            self.__candidates += [
                {
                    "word": bufnames[winnr - 1],
                    "abbr": f"{tabnr}: [{winnr}/{max_winnr}] {winmark(winnr)} {bufnames[winnr-1]}",
                    "action__tabnr": tabnr,
                    "action__winnr": winnr,
                }
            ]
