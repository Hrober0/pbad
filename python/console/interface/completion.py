from collections.abc import Iterable, Mapping

from prompt_toolkit.completion import CompleteEvent, Completer, Completion
from prompt_toolkit.document import Document

from .command import Command
from .config import COMMANDS, LEVELS


class CommandCompleter(Completer):
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> Iterable[Completion]:
        command, space, argument = document.text_before_cursor.partition(" ")
        if not space:
            yield from self._matching(COMMANDS, command)
        elif command == Command.CONTEXT:
            yield from self._matching(LEVELS, argument)

    @staticmethod
    def _matching(options: Mapping[str, str], typed: str) -> Iterable[Completion]:
        for option, description in options.items():
            if option.lower().startswith(typed.lower()):
                yield Completion(
                    option,
                    start_position=-len(typed),
                    display_meta=description,
                )
