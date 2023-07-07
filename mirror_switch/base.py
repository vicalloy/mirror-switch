import sys
from collections.abc import Iterable

from mirror_switch.utils import get_command_name, list_question

from .mirrors import mirrors


class BaseMirror:
    commands: Iterable[str] = []

    @classmethod
    def get_description(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_cmd_name(cls) -> str:
        cmd = get_command_name(cls.commands)
        assert cmd is not None
        return cmd

    @classmethod
    def get_mirror_list(cls) -> list[str | tuple[str, str]]:
        name = cls.__name__[: -len("Mirror")]
        return mirrors[name] + [
            ("Show current config", "show"),
            ("Exit", "exit"),
        ]

    def show_config(self) -> None:
        pass

    def do_set_mirror(self, mirror: str):
        pass

    def set_mirror(self) -> None:
        mirrors = self.get_mirror_list()
        mirror = list_question("Choose a mirror", mirrors)
        if mirror == "exit":
            sys.exit(0)
        if mirror == "show":
            self.show_config()
            self.set_mirror()
            return
        self.do_set_mirror(mirror)
