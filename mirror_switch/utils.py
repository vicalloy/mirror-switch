from collections.abc import Iterable, Sequence
from shutil import which

import inquirer


def list_question(message: str, choices: Sequence[str | tuple[str, str]]) -> str:
    questions = [
        inquirer.List(
            "data",
            message=message,
            choices=choices,
        ),
    ]

    return inquirer.prompt(questions)["data"]


def get_command_name(commands: Iterable[str]) -> str | None:
    return next((cmd for cmd in commands if which(cmd) is not None), None)
