from textual.containers import Container, Horizontal
from textual.app import ComposeResult
from textual.widgets import Markdown, TabbedContent, TabPane, Rule, Button

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
                    yield Markdown(f"## Document ID:{document["id"]}\n**From:** {document["sender"]}\n\n**Title:** {document["title"]}\n\n")
                    yield Rule()
                    yield Markdown("## Content\n" + document["content"])
                    yield Rule()
                    yield Horizontal(
                        Button.success("Approve",   id=f"doc--{document['id']}--approve"),
                        Button.warning("Escalate",  id=f"doc--{document['id']}--escalate"),
                        id = f"{document["id"]}-actions"
                    )

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab
        update_status(self.data, tab.split("--")[-2], "read")
        save_documents(self.data)

    
    def on_button_pressed(self, event: Button.Pressed):
        button_id = event.button.id
        if not button_id:
            return
        if "doc--" not in button_id: 
            return
        
        document_id, action = button_id.split("--")[-2:]
        if action in ("approve","escalate"):
            update_action(self.data, document_id, action)
        
        save_documents(self.data)

        event.stop()
