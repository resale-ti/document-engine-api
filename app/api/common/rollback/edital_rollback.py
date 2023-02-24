from core.rollbar_celery import rollbar_celery
from api.common.repositories.user_repository import UserRepository
from api.common.repositories.history_repository import HistoryRepository
from api.common.repositories.wallet_repository import WalletRepository


class EditalRollback:
    def __init__(self, task_payload: dict) -> None:
        self.payload = task_payload
        self.wallet_id = self.payload.get("id_obj")

    def handler(self) -> None:
        self.__send_message_rollbar()

        HistoryRepository().insert_wallet_history(fields={
            "documento_status": {"new": "failed"},
            "description": "Documento FAILED (Falha na geração do Edital)"}, wallet_id=self.wallet_id)


    def __send_message_rollbar(self):
        user = UserRepository().get_user_detail(
            user_id=self.payload.get("requester_id"))
        carteira = WalletRepository().get_wallet_gestor_detail(wallet_id=self.wallet_id)
        rollbar_celery.report_message(
            f'Edital. Carteira = {carteira.codigo}, Gestor = {carteira.gestor_nome}', 'info')