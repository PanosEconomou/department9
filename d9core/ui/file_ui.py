from textual.app import ComposeResult
from textual.reactive import Reactive
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Markdown, TabbedContent, TabPane, Rule, Static, Button, Input, Sparkline

from d9core.engine.file_manager import get_documents, update_action, update_notes, save_documents, get_entry

class DocumentView(Container):

    data = get_documents()
    progress: Reactive[list[float]] = Reactive([0.5 if document["action"] == "approve" else 1 if document["action"] == "escalate" else 0 for document in data])

    def compose(self) -> ComposeResult:

        if not self.data:
            yield Markdown("No documents yet.")
            return
        with Vertical():
            with TabbedContent(initial=self.data[-1]["id"], id="document-tabs"):
                for document in self.data:
                    if document["available"] != "True":
                        continue
                    with TabPane(document["id"],id=document["id"]) as pane:
                        with Vertical():
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
                        with Vertical():
                            yield Static("" if document["notes"] == "" else f"[bold]Escalation note saved:[/bold]\n{document["notes"]}", id=f"{document["id"]}--feedback")
                            yield Input(
                                placeholder="Enter escalation description…",
                                id=f"{document["id"]}--input",
                                disabled=True
                            )
            yield Sparkline(self.progress,id="progress-line")

    def on_mount(self) -> None:
        if not self.data:
            return
        
        for document in self.data:
            if document["available"] != "True":
                    continue
            input = self.query_one(f"#{document["id"]}--input",Input)
            input.styles.display = "none"

            if document["action"] != "":
                pane = self.query_one(f"#{document["id"]}",TabPane)
                pane.add_class(document["action"])
                tab_btn = self.query_one(f"#--content-tab-{document["id"]}")
                tab_btn.add_class(document["action"])

    def on_show(self) -> None:
        self.query_one(f"#tabs-scroll").parent.focus() # type: ignore

    def spark_update(self) -> None:
        self.progress = [0.5 if document["action"] == "approve" else 1 if document["action"] == "escalate" else 0 for document in self.data]
        progress_bar = self.query_one("#progress-line",Sparkline)
        progress_bar.data = self.progress
        progress_bar.refresh()

    def process_action(self, document_id, action) -> None:
        if get_entry(self.data, document_id)["action"] != "":
            return
        
        update_action(self.data, document_id, action)
        save_documents(self.data)

        feedback = self.query_one(f"#doc--{document_id}--feedback", Static)
        feedback.update(f"[bold]{action.upper()}[/bold] recorded for {document_id}")

        pane = self.query_one(f"#{document_id}",TabPane)
        pane.remove_class("approve", "escalate")
        pane.add_class(action)
        
        tab_btn = self.query_one(f"#--content-tab-{document_id}")
        tab_btn.remove_class("approve", "escalate")
        tab_btn.add_class(action)

        for acn in ("approve", "escalate"):
            button = self.query_one(f"#doc--{document_id}--{acn}", Button)
            button.disabled = True

        if action == "escalate":
            input = self.query_one(f"#{document_id}--input",Input)
            input.styles.display = "block"
            input.disabled = False
            input.focus()

        else:
            self.query_one(f"#tabs-scroll").parent.focus() # type: ignore

        self.spark_update()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if not button_id:
            return
        if "doc--" not in button_id: 
            return
        
        document_id, action = button_id.split("--")[-2:]
        if action in ("approve","escalate"):
            self.process_action(document_id,action)
            event.stop()


    def on_input_submitted(self, event: Input.Submitted) -> None:
            input = event.input
            if not input.id:
                return
            
            if not input.id.endswith("--input"):
                return

            document_id = input.id.split("--")[0]
            note = event.value.strip()
            if not note:
                input_widget = event.input
                input_widget.add_class("invalid")      # style as error
                return
    
            if note:
                update_notes(self.data, document_id, note)
                save_documents(self.data)

            input.disabled = True
            input.styles.display = "none"

            feedback = self.query_one(f"#{document_id}--feedback", Static)
            feedback.update(f"[bold]Escalation note saved:[/bold]\n{note}")

            self.query_one(f"#tabs-scroll").parent.focus() # type: ignore
            
            event.stop()
