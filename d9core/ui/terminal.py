from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Static


class Terminal(App):

    CSS_PATH = "terminal.tcss"
    BINDINGS = [("d", "toggle_dark" ,"Toggle Dark Mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Horizontal(
            VerticalScroll(
                Static("Menu", classes="header"),
                Button("Information"),
                Button("Documents"),
                Button("Email"),
                Button("Secure Messaging")
            )
        )

    def on_mount(self) -> None:
        self.title      = "Depratment 9"
        self.sub_title  = "Remote Access Console"

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

def run_terminal() -> None:
    app = Terminal()
    app.run()