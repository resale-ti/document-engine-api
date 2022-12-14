from api.common.repositories.property_repository import PropertyRepository


class ConditionsRegulamento:

    def __init__(self, payload: dict) -> None:
        self.wallet_id = payload.get('id_obj')
        self.manager_id = payload.get('manager_id')
        self.data_fim = payload.get('data_fim')

    def execute_pre_conditions(self):
        properties = PropertyRepository().get_properties_order_by_address(
            wallet_id=self.wallet_id)

        for idx, prop in enumerate(properties):
            update_data = {"data_limite": self.data_fim, "lote": idx+1}
            history_data = self.__mount_history(prop, update_data)
            PropertyRepository().update_property(property_id=prop.imovel_id, data=update_data,
                                                 history_data=history_data, insert_history=True)

    def __mount_history(self, prop, update_data):
        history_data = {
            "data_limite": {
                "old": prop.data_limite,
                "new": update_data.get("data_limite")
            },
            "lote": {
                "old": int(prop.lote) if prop.lote else "",
                "new": update_data.get("lote")
            },
            "description": f"Geração de Regulamento p/ Carteira {prop.codigo}"
        }

        return history_data
