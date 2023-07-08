import sys
from collections.abc import Callable, Iterable
from pathlib import Path

from mirror_switch.utils import get_command_name, get_first_exists_file, list_question

from .mirrors import mirrors


class BaseMirror:
    commands: Iterable[str] = []
    config_files: Iterable[str] = []

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
    def get_config_file(cls) -> Path:
        fn = get_first_exists_file(cls.config_files)
        assert fn is not None
        return Path(fn)

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

    def handle_menu_action(self, action) -> bool:
        if action in {"show", "s"}:
            self.show_config()
            self.set_mirror()
            return True
        if action in {"back", "b"}:
            self.back_func()
            return True
        if action in {"exit", "q"}:
            sys.exit(0)
        return False

    def set_mirror(self) -> None:
        mirror_list = self.get_mirror_list()
        mirror = list_question("Choose a mirror", mirror_list)
        if self.handle_menu_action(mirror):
            return
        self.do_set_mirror(mirror)
        print(f"Change mirror to: {mirror}")
        self.back_func()
