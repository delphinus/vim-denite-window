import json
import os

from pynvim import attach, setup_logging
from pytest import fixture


setup_logging("test")


@fixture
def vim():
    child_argv = os.environ.get("NVIM_CHILD_ARGV")
    listen_address = os.environ.get("NVIM_LISTEN_ADDRESS")
    if child_argv is None and listen_address is None:
        child_argv = '["nvim", "-u", "NONE", "--embed", "--headless"]'

    if child_argv is not None:
        vim = attach("child", argv=json.loads(child_argv))
    else:
        assert listen_address is None or listen_address != ""
        vim = attach("socket", path=listen_address)

    yield vim

    if len(vim.tabpages) > 2:
        for tabpage in vim.tabpages[1 : len(vim.tabpages)]:
            vim.current.tabpage(tabpage)
            vim.command("tabclose")

    vim.command("only")
    vim.command("enew")
