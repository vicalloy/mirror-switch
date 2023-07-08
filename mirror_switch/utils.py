from collections.abc import Iterable, Sequence
from pathlib import Path
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


def text_question(message: str) -> str:
    questions = [
        inquirer.Text(
            "data",
            message=message,
        ),
    ]

    return inquirer.prompt(questions)["data"]


def get_command_name(commands: Iterable[str]) -> str | None:
    return next((cmd for cmd in commands if which(cmd) is not None), None)


def get_first_exists_file(files: Iterable[str]) -> str | None:
    return next((file for file in files if Path(file).expanduser().exists()), None)
