import pyperclip
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape
from rich.console import Console, RenderableType
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

from llm import Chat, ContextLevel, SqlAnswer, SqlGenerator, Tokens

from .command import Command
from .completion import CommandCompleter
from .config import MODE_COLORS
from .mode import Mode


class Repl:
    def __init__(self, chat: Chat, sql: SqlGenerator) -> None:
        self._chat = chat
        self._sql = sql
        self._console = Console()
        self._prompt = self._create_prompt()
        self._mode = Mode.CHAT
        self._level = ContextLevel.K0

    def run(self) -> None:
        self._console.rule("[bold cyan]Claude Interface", style="cyan")
        self._console.print("[dim]Type / to see commands[/]", justify="center")

        while True:
            self._console.print()
            question = self._prompt.prompt(
                [("ansicyan bold", f"{self._label()} > ")]
            ).strip()
            if not question:
                continue

            command, _, argument = question.partition(" ")
            if command == Command.EXIT:
                break
            if command == Command.MODE:
                self._switch_mode()
            elif command == Command.CONTEXT:
                self._switch_level(argument.strip())
            elif question.startswith("/"):
                self._console.print(
                    "[red]Slash starts a command, not a prompt."
                    " Type / to see the available ones.[/]"
                )
            elif self._mode is Mode.SQL:
                self._show_sql(question)
            else:
                self._show_answer(question)

    def _create_prompt(self) -> PromptSession:
        return PromptSession(
            placeholder=[("ansibrightblack", "Type your prompt...")],
            cursor=CursorShape.BEAM,
            completer=CommandCompleter(),
            complete_while_typing=True,
        )

    def _label(self) -> str:
        return f"{self._mode} {self._level}" if self._mode is Mode.SQL else self._mode

    def _switch_mode(self) -> None:
        self._mode = Mode.SQL if self._mode is Mode.CHAT else Mode.CHAT
        self._console.print(f"[dim]Switched to {self._label()} mode[/]")

    def _switch_level(self, argument: str) -> None:
        self._level = ContextLevel(argument.upper()) if argument else self._level.next
        self._console.print(f"[dim]Context level set to {self._level}[/]")

    def _panel(
        self,
        body: RenderableType,
        tokens: Tokens | None,
        level: ContextLevel | None,
    ) -> Panel:
        suffix = f" · {level}" if level else ""
        usage = (
            f"[dim]prompt {tokens.prompt} · output {tokens.output}[/]"
            if tokens
            else None
        )
        return Panel(
            renderable=body,
            title=f"Claude [dim]({self._chat.config.model}{suffix})[/]",
            title_align="left",
            subtitle=usage,
            subtitle_align="right",
            border_style=MODE_COLORS[self._mode],
        )

    def _render(self, answer: str, tokens: Tokens | None = None) -> Panel:
        return self._panel(Markdown(answer), tokens, None)

    def _render_sql(self, answer: SqlAnswer) -> Panel:
        body = Syntax(answer.pretty, "json", theme="ansi_dark", word_wrap=True)
        return self._panel(body, answer.tokens, answer.level)

    def _show_sql(self, question: str) -> None:
        status = f"[yellow]Generating SQL with {self._level}..."
        with self._console.status(status, spinner="dots"):
            answer = self._sql.generate(question, self._level)

        self._console.print(self._render_sql(answer))
        pyperclip.copy(answer.sql)
        self._console.print("[dim]Query copied to clipboard[/]")

    def _show_answer(self, question: str) -> None:
        with self._console.status("[cyan]Thinking...", spinner="dots"):
            chunks = self._chat.ask(question)
            answer = next(chunks, "")

        with Live(self._render(answer), console=self._console) as live:
            for chunk in chunks:
                answer += chunk
                live.update(self._render(answer))
            live.update(self._render(answer, self._chat.tokens))
