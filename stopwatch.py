from textual.app import App, ComposeResult
from textual.widgets import Button, Digits, Footer, Header
from textual.containers import HorizontalGroup, VerticalScroll


class TimeDisplay(Digits):
    """A widget to display elapsed time."""
    pass


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def compose(self) -> ComposeResult:
        """Create child widgets for the stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay("00:00:00:00")


class StopwatchApp(App):
    """A textual stopwatch app."""

    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(icon="", show_clock=True)
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch())

    def on_mount(self) -> None:
        self.title = "Stopwatch"
        self.sub_title = "As per textual tutorial"

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

    def action_quit(self) -> None:
        """An action to quit the app."""
        self.exit()


if __name__ == "__main__":
    app = StopwatchApp()
    app.run()
