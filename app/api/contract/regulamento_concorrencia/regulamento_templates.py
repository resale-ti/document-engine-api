import os
from pathlib import Path
from tkinter.messagebox import NO
from xml.dom.minidom import Document


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


class MLP002:

    folder = "MLP_002"
    template_path = template_path
    stylesheets = "regulamento.css"

    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data

    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes