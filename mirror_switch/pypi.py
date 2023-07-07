import subprocess

from mirror_switch.base import BaseMirror
from mirror_switch.utils import get_command_name


def get_pip() -> str:
    cmd = get_command_name(["pip", "pip3"])
    assert cmd is not None
    return cmd


class PypiMirror(BaseMirror):
    @classmethod
    def get_description(cls) -> str:
        return "PyPI"

    def show_config(self) -> None:
        pip = get_pip()
        cmd = (pip, "config", "list")
        subprocess.call(cmd)

    def do_set_mirror(self, mirror: str):
        pip = get_pip()
        cmd = (pip, "config", "set", "global.index-url", mirror)
        subprocess.call(cmd)
