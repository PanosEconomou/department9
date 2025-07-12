from d9core.engine.file_manager import get_documents
from textual.app import App, ComposeResult
from textual.widgets import Label, Markdown, TabbedContent, TabPane

class DocumentView(App):

    data = get_documents()

    def compose(self) -> ComposeResult:
        with TabbedContent():
            for document in self.data:
                with TabPane(document["id"],id=document["id"]):
                    yield Markdown(document["content"])


if __name__ == "__main__":
    DocumentView().run()