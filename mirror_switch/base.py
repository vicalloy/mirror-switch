import sys

from mirror_switch.utils import list_question

from .mirrors import mirrors


class BaseMirror:
    @property
    def description(self) -> str:
        raise NotImplementedError

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
        self.do_set_mirror(mirror)
