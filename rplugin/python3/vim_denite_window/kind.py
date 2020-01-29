from typing import Tuple
from operator import itemgetter
from denite.util import Nvim, Candidate, Candidates


class Window:
    def __init__(self, vim: Nvim) -> None:
        self.vim = vim

    def open(self, target: Candidate) -> None:
        (tabnr, winnr) = self._action_props(target)
        buffers = self.vim.call("tabpagebuflist", tabnr)
        bufnr = buffers[winnr - 1]
        self.vim.command(f"buffer {bufnr}")

    def jump(self, target: Candidate) -> None:
        (tabnr, winnr) = self._action_props(target)
        self.vim.command(f"tabnext {tabnr}")
        self.vim.command(f"{winnr}wincmd w")

    def only(self, target: Candidate) -> None:
        self.jump(target)
        self.vim.command("only")

    def delete(self, targets: Candidates) -> None:
        current_tabnr = self.vim.call("tabpagenr")

        for target in sorted(
            targets, key=itemgetter("action__tabnr", "action__winnr"), reverse=True,
        ):
            self.jump(target)
            self.vim.command("close")

        if current_tabnr != self.vim.call("tabpagenr"):
            self.vim.command(f"tabnext {current_tabnr}")

    def _action_props(self, target: Candidate) -> Tuple[int, int]:
        return target["action__tabnr"], target["action__winnr"]
