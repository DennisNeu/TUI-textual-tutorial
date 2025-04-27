from time import monotonic

from textual.app import App, ComposeResult
from textual.widgets import Button, Digits, Footer, Header
from textual.containers import HorizontalGroup, VerticalScroll
from textual.reactive import reactive


class TimeDisplay(Digits):
    """A widget to display elapsed time."""
    start_time = reactive(monotonic)
    time = reactive(0.0)
    total = reactive(0.0)

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_timer = self.set_interval(1/60, self.update_time, pause=True)

    def update_time(self) -> None:
        """Method to update the time to the current time."""
        self.time = self.total + (monotonic() - self.start_time)
    
    def watch_time(self, time: float) -> None:
        """Called when the time attribute changes."""
        minutes, seconds = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)
        self.update(f"{hours:02,.0f}:{minutes:02.0f}:{seconds:05.2f}")

    def start(self) -> None:
        """Method to start or resume the timer."""
        self.start_time = monotonic()
        self.update_timer.resume()

    def stop(self) -> None:
        """Method to stop the timer."""
        self.update_timer.pause()
        self.total += monotonic() - self.start_time
        self.time = self.total

    def reset(self) -> None:
        """Method to reset the time display to zero."""
        self.total = 0
        self.time = 0


class Stopwatch(HorizontalGroup):
    """A stopwatch widget."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        time_display = self.query_one(TimeDisplay)
        if button_id == "start":
            time_display.start()
            self.add_class("started")
        elif button_id == "stop":
            time_display.stop()
            self.remove_class("started")
        elif button_id == "reset":
            time_display.reset()

    def compose(self) -> ComposeResult:
        """Create child widgets for the stopwatch."""
        yield Button("Start", id="start", variant="success")
        yield Button("Stop", id="stop", variant="error")
        yield Button("Reset", id="reset")
        yield TimeDisplay()


class StopwatchApp(App):
    """A textual stopwatch app."""

    CSS_PATH = "stopwatch.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit", "Quit"),
        ("a", "add_stopwatch", "Add stopwatch"),
        ("r", "remove_stopwatch", "Remove stopwatch"),
        ]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(icon="", show_clock=True)
        yield Footer()
        yield VerticalScroll(Stopwatch(), Stopwatch(), Stopwatch(), id="timers")

    def on_mount(self) -> None:
        self.title = "Stopwatch"
        self.sub_title = "As per textual tutorial"

    def action_addstopwatch(self) -> None:
        """An action to add a new stopwatch."""
        new_stopwatch = Stopwatch()
        self.query_one("#timers").mount(new_stopwatch)
        new_stopwatch.scroll_visible()

    def action_remove_stopwatch(self) -> None:
        """An action to remove the last stopwatch."""
        timers = self.query("Stopwatch")
        if timers:
            timers.last().remove()

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
