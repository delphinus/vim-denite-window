import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

from vim_denite_window.source import Window
from denite.base.source import Base
from denite.util import Nvim, UserContext, Candidate, Candidates


class Source(Base):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = "dwm"
        self.kind = "dwm"
        self.__candidates: Candidates = []
        self.__source = Window(vim)

    def on_init(self, context: UserContext) -> None:
        current_tabnr = self.vim.call("tabpagenr")
        self.__candidates = self.__source.get_windows(current_tabnr)

    def gather_candidates(self, context: UserContext) -> Candidates:
        return self.__candidates

    def highlight(self) -> None:
        self.__source.highlight(self.syntax_name)
