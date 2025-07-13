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
                if document["available"] != "True":
                    continue
                with TabPane(document["id"],id=document["id"]):
                    yield Static(f"[bold]Document ID:[/bold] {document["id"]}")
                    yield Static(f"[bold]From:[/bold] {document["sender"]}")
                    yield Static(f"[bold]Title:[/bold] {document["title"]}")
                    yield Rule()
                    yield Markdown("# Content\n" + document["content"])
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

            pane = self.query_one(f"#{document_id}",TabPane)
            pane.remove_class("approve", "escalate")
            pane.add_class(action)
            pane.TabPaneMessage

            tab_btn = self.query_one(f"#--content-tab-{document_id}")
            print("HIIIIII!: ",tab_btn._selector_names)
            tab_btn.remove_class("approve", "escalate")
            tab_btn.add_class(action)

            for action in ("approve", "escalate"):
                button = self.query_one(f"#doc--{document_id}--{action}", Button)
                button.disabled = True

            event.stop()
