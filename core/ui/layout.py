from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


class Layout(App):

    BINDINGS = [("d", "toggle_dark" ,"Toggle Dark Mode")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

if __name__ == "__main__":
    app = Layout()
    app.run()