from textual.containers import Container, Horizontal
from textual.app import ComposeResult
from textual.widgets import Markdown, TabbedContent, TabPane, Rule, Static, Button

from d9core.engine.file_manager import get_documents, update_action, update_status, save_documents

class DocumentView(Container):

    data = get_documents()

    def compose(self) -> ComposeResult:

        if not self.data:
            yield Markdown("No documents yet.")
            return
        
        with TabbedContent(initial=self.data[0]["id"]):
            for document in self.data:
                with TabPane(document["id"],id=document["id"]):
                    yield Static(f"[bold]Document ID:[/bold] {document["id"]}")
                    yield Static(f"[bold]From:[/bold] {document["sender"]}")
                    yield Static(f"[bold]Title:[/bold] {document["title"]}")
                    yield Rule()
                    yield Markdown("## Content\n" + document["content"])
                    yield Rule()
                    yield Static("" if document["action"] == "" else f"[bold]{document["action"].upper()}[/bold] recorded for {document["id"]}", id=f"doc--{document['id']}--feedback")
                    yield Horizontal(
                        Button.success("Approve",   id=f"doc--{document['id']}--approve",   disabled=document["action"] != ""),
                        Button.warning("Escalate",  id=f"doc--{document['id']}--escalate",  disabled=document["action"] != ""),
                        id = f"{document["id"]}-actions"
                    )
                    
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if not button_id:
            return
        if "doc--" not in button_id: 
            return
        
        document_id, action = button_id.split("--")[-2:]
        if action in ("approve","escalate"):
            update_action(self.data, document_id, action)
            save_documents(self.data)

            feedback = self.query_one(f"#doc--{document_id}--feedback", Static)
            feedback.update(f"[bold]{action.upper()}[/bold] recorded for {document_id}")

            for action in ("approve", "escalate"):
                button = self.query_one(f"#doc--{document_id}--{action}", Button)
                button.disabled = True

            event.stop()
