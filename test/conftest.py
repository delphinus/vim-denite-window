import json
import os

from pynvim import attach, setup_logging
from pytest import fixture

import logging

setup_logging("test")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@fixture
def vim() -> None:
    child_argv = os.environ.get("NVIM_CHILD_ARGV")
    listen_address = os.environ.get("NVIM_LISTEN_ADDRESS")
    if child_argv is None and listen_address is None:
        child_argv = '["nvim", "-u", "NONE", "-i", "NONE", "--embed", "--headless"]'

    if child_argv is not None:
        vim = attach("child", argv=json.loads(child_argv))
    else:
        assert listen_address is None or listen_address != ""
        vim = attach("socket", path=listen_address)

    vim.command("autocmd BufEnter :set bufhidden=wipe<CR>")

    yield vim

    logger.info("teardown")

    if len(vim.windows) > 1:
        for window in vim.windows[1 : len(vim.windows)]:
            vim.current.window = window
            vim.command("close")

    vim.command("enew")
