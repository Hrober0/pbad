from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.cursor_shapes import CursorShape
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from llm import Chat

from .command import Command
from .config import COMMANDS, MODE_COLORS
from .mode import Mode


class Repl:
    def __init__(self, chat: Chat) -> None:
        self._chat = chat
        self._console = Console()
        self._prompt = self._create_prompt()
        self._mode = Mode.CHAT

    def run(self) -> None:
        self._console.rule("[bold cyan]Claude Interface", style="cyan")
        self._console.print("[dim]Type / to see commands[/]", justify="center")

        while True:
            self._console.print()
            question = self._prompt.prompt(
                [("ansicyan bold", f"{self._mode} > ")]
            ).strip()
            if not question:
                continue
            if question == Command.EXIT:
                break
            if question == Command.MODE:
                self._switch_mode()
            elif self._mode is Mode.SQL:
                self._console.print(self._render("SQL mode is coming soon."))
            else:
                self._show_answer(question)

    def _create_prompt(self) -> PromptSession:
        return PromptSession(
            placeholder=[("ansibrightblack", "Type your prompt...")],
            cursor=CursorShape.BEAM,
            completer=WordCompleter(list(COMMANDS), meta_dict=COMMANDS, sentence=True),
            complete_while_typing=True,
        )

    def _switch_mode(self) -> None:
        self._mode = Mode.SQL if self._mode is Mode.CHAT else Mode.CHAT
        self._console.print(f"[dim]Switched to {self._mode} mode[/]")

    def _render(self, answer: str) -> Panel:
        return Panel(
            renderable=Text(answer) if self._mode is Mode.SQL else Markdown(answer),
            title=f"Claude [dim]({self._chat.config.model})[/]",
            title_align="left",
            border_style=MODE_COLORS[self._mode],
        )

    def _show_answer(self, question: str) -> None:
        with self._console.status("[cyan]Thinking...", spinner="dots"):
            chunks = self._chat.ask(question)
            answer = next(chunks, "")

        with Live(self._render(answer), console=self._console) as live:
            for chunk in chunks:
                answer += chunk
                live.update(self._render(answer))
