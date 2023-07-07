import subprocess

from mirror_switch.base import BaseMirror


class NpmMirror(BaseMirror):
    commands = ["npm"]

    @classmethod
    def get_description(cls) -> str:
        return "npm"

    def show_config(self) -> None:
        npm = self.get_cmd_name()
        cmd = (npm, "config", "get", "registry")
        subprocess.call(cmd)

    def do_set_mirror(self, mirror: str):
        yarn = self.get_cmd_name()
        cmd = (yarn, "config", "set", "registry", mirror)
        subprocess.call(cmd)
