import sys
from collections.abc import Callable, Iterable

from mirror_switch.utils import get_command_name, list_question

from .mirrors import mirrors


class BaseMirror:
    commands: Iterable[str] = []

    def __init__(self, back_func: Callable):
        self.back_func = back_func

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
            ("Back", "back"),
            ("Exit", "exit"),
        ]

    def show_config(self) -> None:
        pass

    def do_set_mirror(self, mirror: str):
        pass

    def set_mirror(self) -> None:
        mirror_list = self.get_mirror_list()
        mirror = list_question("Choose a mirror", mirror_list)
        if mirror == "show":
            self.show_config()
            self.set_mirror()
            return
        if mirror == "back":
            self.back_func()
            return
        if mirror == "exit":
            sys.exit(0)
        self.do_set_mirror(mirror)
