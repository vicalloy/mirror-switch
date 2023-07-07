import sys

from mirror_switch.base import BaseMirror

from .pypi import PypiMirror
from .utils import list_question


def get_mirror_type() -> BaseMirror:
    message = "What type of mirror do you need?"
    choices = [(cls.get_description(), cls.__name__) for cls in [PypiMirror]]
    choices.append(("Exit", "exit"))
    cls_name = list_question(message, choices)
    if cls_name == "exit":
        sys.exit(0)
    return globals()[cls_name]()


def main():
    mirror_type_module = get_mirror_type()
    mirror_type_module.set_mirror()


if __name__ == "__main__":
    main()
