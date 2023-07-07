from mirror_switch.npm import NpmMirror


class YarnMirror(NpmMirror):
    commands = ["yarn"]

    @classmethod
    def get_description(cls) -> str:
        return "Yarn"
