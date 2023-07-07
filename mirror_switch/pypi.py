import subprocess

from mirror_switch.base import BaseMirror


class PypiMirror(BaseMirror):
    commands = ["pip", "pip3"]

    @classmethod
    def get_description(cls) -> str:
        return "PyPI"

    def show_config(self) -> None:
        pip = self.get_cmd_name()
        cmd = (pip, "config", "get", "global.index-url")
        subprocess.call(cmd)

    def do_set_mirror(self, mirror: str):
        pip = self.get_cmd_name()
        cmd = (pip, "config", "set", "global.index-url", mirror)
        subprocess.call(cmd)
