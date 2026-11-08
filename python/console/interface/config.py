from llm import ContextLevel

from .command import Command
from .mode import Mode

COMMANDS: dict[Command, str] = {
    Command.MODE: "Switch between chat and SQL mode",
    Command.CONTEXT: "Pick the context level for SQL mode",
    Command.EXIT: "Close the interface",
}

LEVELS: dict[ContextLevel, str] = {
    ContextLevel.K0: "Table and column names",
    ContextLevel.K1: "K0 + types, keys and geometries",
    ContextLevel.K2: "K1 + descriptions, fclass values and facts",
    ContextLevel.K3: "K2 + query hints and examples",
}

MODE_COLORS: dict[Mode, str] = {
    Mode.CHAT: "magenta",
    Mode.SQL: "yellow",
}
