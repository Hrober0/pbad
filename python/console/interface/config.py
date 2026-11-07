from .command import Command
from .mode import Mode

COMMANDS: dict[Command, str] = {
    Command.MODE: "Switch between chat and SQL mode",
    Command.EXIT: "Close the interface",
}

MODE_COLORS: dict[Mode, str] = {
    Mode.CHAT: "magenta",
    Mode.SQL: "yellow",
}
