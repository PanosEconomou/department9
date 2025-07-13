from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Button, Static, ContentSwitcher, TabbedContent

from d9core.ui.file_ui import DocumentView


class Terminal(App):

    CSS_PATH = "terminal.tcss"
    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("a", "approve", "Accept Document"),
        ("e", "escalate", "Escalate Document"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Horizontal(id="main-view"):
            with VerticalScroll(id="buttons"):
                yield Button("Information", id="information-view")
                yield Button("Documents", id="document-view")
                yield Button("Email", id="email-view")
                yield Button("Secure Messaging", id="messaging-view")
            with ContentSwitcher(initial="information-view", id="content-view"):
                yield Static("Information View Coming Soon...", id="information-view")
                yield DocumentView(id="document-view")
                yield Static("Email View Coming Soon...", id="email-view")
                yield Static("Secure Messaging View Coming Soon...", id="messaging-view")

    def on_mount(self) -> None:
        self.title      = "Depratment 9"
        self.sub_title  = "Remote Access Console"

    def on_button_pressed(self, event:Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id
        self.refresh_bindings()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )
    
    def action_approve(self) -> None:
        documents = self.query_one("#document-view",DocumentView)
        document_id = documents.query_one("#document-tabs",TabbedContent).active
        documents.process_action(document_id,"approve")

    def action_escalate(self) -> None:
        documents = self.query_one("#document-view",DocumentView)
        document_id = documents.query_one("#document-tabs",TabbedContent).active
        documents.process_action(document_id,"escalate")

    def check_action(self, action: str, parameters: tuple[object, ...]) -> bool | None:
        try:
            content = self.query_one(ContentSwitcher).current
            if action == "approve" and content != "document-view":
                return False
            if action == "escalate" and content != "document-view":
                return False
        except:
            return False
        
        return True


def run_terminal() -> None:
    app = Terminal()
    app.run()