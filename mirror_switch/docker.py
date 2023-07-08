import json
import platform
import subprocess
import tempfile
from pathlib import Path
from pprint import pp

from mirror_switch.base import BaseMirror
from mirror_switch.utils import text_question


class DockerMirror(BaseMirror):
    commands = ["docker"]

    @classmethod
    def get_description(cls) -> str:
        return "Docker"

    @classmethod
    def get_config_file(cls) -> Path:
        if platform.system() == "Darwin":  # Mac
            fn = "~/.docker/daemon.json"
        else:
            fn = "/etc/docker/daemon.json"  # Linux
        return Path(fn).expanduser()

    def show_config(self) -> None:
        config_file = self.get_config_file()
        if not config_file.exists():
            print("Config file not found")
            return
        with open(config_file) as f:
            config: dict = json.load(f)
            pp(config.get("registry-mirrors", []))

    def set_mirror(self) -> None:
        mirror_list = self.get_mirror_list()[:-3]
        for i, mirror in enumerate(mirror_list):
            print(f"{i} {mirror}")
        print("s Show current config")
        print("q Quit/Exit")
        print("b Back")
        mirror_ids = text_question("Choose mirrors(ex: 1,2,3)").strip()
        if self.handle_menu_action(mirror_ids):
            return
        try:
            selected_mirrors = [mirror_list[int(i)] for i in mirror_ids.split(",")]
        except (ValueError, IndexError):
            print("Invalid input, please input mirrors id(ex: 1,2,3)")
            self.set_mirror()
            return
        self.do_set_mirrors(selected_mirrors)  # type: ignore
        print("Docker registry mirrors updated. Please restart the daemon.")

    def do_set_mirrors(self, mirrors: list[str]):
        config_file = self.get_config_file()
        tmp_dir = Path(tempfile.gettempdir())
        tmp_file = tmp_dir / "daemon.json"
        config = {}
        if config_file.exists():
            subprocess.call(["cp", config_file, tmp_file])
            with open(tmp_file) as f:
                config = json.load(f)
        config["registry-mirrors"] = mirrors
        print("Config file:", tmp_file)
        with open(tmp_file, "w") as f:
            json.dump(config, f, indent=2)
        if platform.system() == "Darwin":  # Mac
            subprocess.call(["cp", tmp_file, config_file])
        else:  # Linux
            subprocess.call(["sudo", "cp", tmp_file, config_file])
