import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

import typing
from denite_window.source import Window
from denite.base.source import Base
from denite.util import Nvim, UserContext, Candidate, Candidates


class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = "window"
        self.kind = "window"
        self.__candidates: Candidates = []
        self.__source = Window(vim)

    def on_init(self, context: UserContext) -> None:
        self.__candidates = []
        current_tabnr = self.vim.call("tabpagenr")
        options = self._options(context)
        if options["all"]:
            max_tabnr = self.vim.call("tabpagenr", "$")
            for tabnr in range(1, max_tabnr + 1):
                need_marks = tabnr == current_tabnr
                no_current = need_marks and options["no-current"]
                self.__candidates += self.__source.get_windows(
                    tabnr, no_current, need_marks
                )
        else:
            self.__candidates = self.__source.get_windows(
                current_tabnr, options["no-current"], True
            )

    def gather_candidates(self, context: UserContext) -> Candidates:
        return self.__candidates

    def highlight(self) -> None:
        self.__source.highlight(self.syntax_name)

    def _options(self, context: UserContext) -> typing.Dict[str, bool]:
        return {
            "no-current": "no-current" in context["args"],
            "all": "all" in context["args"],
        }
