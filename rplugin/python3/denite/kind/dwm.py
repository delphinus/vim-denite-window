import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))

from vim_denite_window.kind import Window
from denite.kind.openable import Kind as Openable
from denite.util import Nvim, UserContext, Candidate


class Kind(Openable):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = "dwm"
        self.default_action = "focus"
        self.redraw_actions += ["delete"]
        self.persist_actions += ["delete"]
        self.__kind = Window(vim)

    def action_focus(self, context: UserContext) -> None:
        self.action_jump(context)
        self.vim.call("DWM_Focus")

    def action_open(self, context: UserContext) -> None:
        self.__kind.open(context["targets"])

    def action_jump(self, context: UserContext) -> None:
        self.__kind.jump(context["targets"][0])

    def action_only(self, context: UserContext) -> None:
        self.__kind.only(context["targets"][0])

    def action_delete(self, context: UserContext) -> None:
        self.__kind.delete(context["targets"])
        self.vim.command("wincmd H")
        self.vim.call("DWM_ResizeMasterPaneWidth")
