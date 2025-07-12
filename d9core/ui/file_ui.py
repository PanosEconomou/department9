from textual.containers import Container
from textual.app import ComposeResult
from textual.widgets import Markdown, TabbedContent, TabPane

from d9core.engine.file_manager import get_documents

class DocumentView(Container):

    def compose(self) -> ComposeResult:

        data = get_documents()

        if not data:
            yield Markdown("No documents yet.")
            return
        
        with TabbedContent(initial=data[0]["id"]):
            for document in data:
                with TabPane(document["id"],id=document["id"]):
                    yield Markdown(document["content"])

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab