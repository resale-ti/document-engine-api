import os

from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.history_repository import HistoryRepository


class RegulamentoRollback:
    def __init__(self, task_payload: dict) -> None:
        self.payload = task_payload

    def handler(self) -> None:
        doc_id = os.environ.get("DOCUMENT_ID_RC")
        print(f"regulamento rollback doc id = {doc_id}")

        if doc_id:
            wallet_id = self.payload.get("id_obj")
            print(f"Failed Regulamento p/ Carteira: {wallet_id}")

            DocumentRepository().failed_regulamento(doc_id)
            HistoryRepository().insert_wallet_history(fields = {
                "documento_status": {"new": "failed"},
                "description": "Documento FAILED (Falha na geração do Regulamento)"}, wallet_id=wallet_id)
