import typing

from denite.kind.openable import Kind as Openable
from denite.util import Nvim, UserContext, Candidate
from operator import attrgetter


class Kind(Openable):
    def __init__(self, vim: Nvim) -> None:
        super().__init__(vim)

        self.name = "window"
        self.default_action = "jump"
        self.redraw_actions += ["delete"]
        self.persist_actions += ["delete", "preview"]

    def action_open(self, context: UserContext) -> None:
        for target in context["targets"]:
            (tabnr, winnr) = self._action_props(target)
            buffers = self.vim.call("tabpagebuflist", tabnr)
            bufnr = buffers[winnr - 1]
            self.vim.command(f"buffer {bufnr}")

    def action_jump(self, context: UserContext) -> None:
        (tabnr, winnr) = self._action_props(context["targets"][0])
        self.vim.command(f"tabnext {tabnr}")
        self.vim.command(f"{winnr}wincmd w")

    def action_only(self, context: UserContext) -> None:
        self.action_jump(context)
        self.vim.command("only")

    def action_delete(self, context: UserContext) -> None:
        current_tabnr = self.vim.call("tabpagenr")

        for target in sorted(
            context["targets"],
            key=attrgetter("action__tabnr", "action__winnr"),
            reverse=True,
        ):
            self.action_jump({"targets": [target]})
            self.vim.command("close")

        if current_tabnr != self.vim.call("tabpagenr"):
            self.vim.command(f"tabnext {current_tabnr}")

    def _action_props(self, target: Candidate) -> (int, int):
        return target["action__tabnr"], target["action__winnr"]
