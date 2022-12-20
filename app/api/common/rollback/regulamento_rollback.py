import os
from datetime import datetime
from core.rollbar_celery import rollbar_celery
from api.common.repositories.user_repository import UserRepository
from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.history_repository import HistoryRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.wallet_repository import WalletRepository


class RegulamentoRollback:
    def __init__(self, task_payload: dict) -> None:
        self.payload = task_payload
        self.wallet_id = self.payload.get("id_obj")

    def handler(self) -> None:
        self.__send_message_rollbar()

        doc_id = os.environ.get("DOCUMENT_ID_RC")

        if doc_id:
            self.__document_handler(doc_id)

        self.__handle_properties()

    def __document_handler(self, doc_id):
        print(f"regulamento rollback doc id = {doc_id}")

        print(f"Failed Regulamento p/ Carteira: {self.wallet_id}")

        DocumentRepository().failed_regulamento(doc_id)
        HistoryRepository().insert_wallet_history(fields={
            "documento_status": {"new": "failed"},
            "description": "Documento FAILED (Falha na geração do Regulamento)"}, wallet_id=self.wallet_id)

    def __handle_properties(self):
        properties = PropertyRepository().get_properties_wallet_with_schedule(
            wallet_id=self.wallet_id)
        data = {"data_limite": None, "lote": None}

        for p in properties:
            print(
                f"Atualizando Data Limite e Lote para o imóvel: {p.idr_imovel}")
            history_data = self.__mount_properties_history(p)
            PropertyRepository().update_property(property_id=p.imovel_id,
                                                 data=data, history_data=history_data)

    # ----------------------------------------------- HELPER -------------------------------------------------
    # --------------------------------------------------------------------------------------------------------

    def __mount_properties_history(self, p):
        history_data = {
            "data_limite": {"old": p.data_limite, "new": None},
            "lote": {"old": int(p.lote) if p.lote else "", "new": None},
            "description": f"Falha na geração de Regulamento p/ Carteira {p.codigo}"
        }

        return history_data

    def __send_message_rollbar(self):
        data_inicio = datetime.strptime(
            self.payload.get("data_inicio"), "%Y-%m-%dT%H:%M:%S")
        data_fim = datetime.strptime(
            self.payload.get("data_fim"), "%Y-%m-%dT%H:%M:%S")

        user = UserRepository().get_user_detail(
            user_id=self.payload.get("requester_id"))
        carteira = WalletRepository().get_wallet_gestor_detail(wallet_id=self.wallet_id)
        rollbar_celery.report_message(
            f'Regulamento. Carteira = {carteira.codigo}, Gestor = {carteira.gestor_nome}, Data Inicio = {data_inicio.strftime("%d/%m/%Y %H:%M")}, Data Fim = {data_fim.strftime("%d/%m/%Y %H:%M")}, Usuário = {user.username}', 'info')