from api.common.database_common import DBSessionContext
from api.common.models import PropertyHistory, WalletHistory
from datetime import datetime
import os


class HistoryRepository(DBSessionContext):
    """
        @params:fields structure =

        fields = {
            "field": {
                "old": old, # NOT REQUIRED
                "new": new
            },
            "description": "Utilidade Pública"
        }
        """

    # ----------------------------------HELPERS FUNCTIONS----------------------------------------------------
    # -------------------------------------------------------------------------------------------------------


    def __validate_body(self, field):
        if not "new" in field.keys():
            raise Exception(
                "É necessário seguir a estruturação padrão para inserção no Histórico.")

    def __get_description_and_requester(self, fields):
        description = fields.pop(
            "description") if "description" in fields else ""
        requester_id = os.environ.get("REQUESTER_ID")

        return description, requester_id

    def __mount_payload(self, field, value, requester_id, description):
        return {"campo": field,
                "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "usuario_id": requester_id if requester_id else 1,
                "valor_antigo": value.get("old"),
                "valor_novo": value.get("new"),
                "descricao": description}

    # -------------------------------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------------------------------

    def insert_property_history(self, imovel_id, fields):
        with self.get_session_scope() as session:
            description, requester_id = self.__get_description_and_requester(fields=fields)

            for field, value in fields.items():
                self.__validate_body(value)

                if value.get("old") == value.get("new"):
                    continue

                payload_imovel = self.__mount_payload(
                    field, value, requester_id, description) | {"imovel_id": imovel_id, "operacao": "update"}

                property_history = PropertyHistory(**payload_imovel)
                session.add(property_history)

    def insert_wallet_history(self, wallet_id, fields):
        with self.get_session_scope() as session:
            description, requester_id = self.__get_description_and_requester(fields=fields)

            for field, value in fields.items():
                self.__validate_body(value)

                if value.get("old") == value.get("new"):
                    continue

                payload_carteira=self.__mount_payload(field, value, requester_id, description) | {
                                                      "carteira_id": wallet_id}

                wallet_history = WalletHistory(**payload_carteira)
                session.add(wallet_history)
