from api.common.database_common import DBSessionContext
from api.common.models import PropertyHistory
from datetime import datetime


class HistoryRepository(DBSessionContext):

    def __validate_body(self, field):
        if not "new" in field.keys():
            raise Exception(
                "É necessário seguir a estruturação padrão para inserção no Histórico.")

    def insert_property_history(self, session, imovel_id, fields, requester_id=1):
        with self.get_session_scope() as session:
            description = fields.pop("description") if "description" in fields else ""

            for field, value in fields.items():
                self.__validate_body(value)

                if value.get("old") == value.get("new"):
                    continue

                payload_imovel = {"imovel_id": imovel_id,
                                  "campo": field,
                                  "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                  "usuario_id": requester_id,
                                  "operacao": "update",
                                  "valor_antigo": value.get("old"),
                                  "valor_novo": value.get("new"),
                                  "descricao": description}

                property_history = PropertyHistory(**payload_imovel)
                session.add(property_history)
