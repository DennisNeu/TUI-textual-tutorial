from textual.app import App, ComposeResult
from textual.widgets import Footer, Header


class StopwatchApp(App):
    """A textual stopwatch app."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

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