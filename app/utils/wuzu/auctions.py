import os
from datetime import timedelta
from utils.wuzu.service import WuzuService
from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository


class Auctions:

    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None

    def handle_auctions(self, task_requests):
        wallet_id = task_requests.get("id_obj")
        regulamento = DocumentRepository().get_active_regulamento_wallet(wallet_id=wallet_id)

        properties = PropertyRepository().get_properties_wallet_to_wuzu(wallet_id)

        self.set_times(properties, task_requests)

        if regulamento:
            self.send_update(properties)
        else:
            self.send_open(wallet_id, properties[0].schedule_id)


    # ------------------------------------------------------------------------------------------

    def send_update(self, properties):
        wuzu_service = WuzuService()

        properties_tuple = tuple([imovel.imovel_id for imovel in properties])
        auctions_ids = PropertyAuctionRepository().get_wuzu_auction_id_by_many_properties(
            properties_tuple, properties[0].schedule_id)

        auctions_ids_list = [dw.wuzu_disputa_id for dw in auctions_ids]

        buffer = []
        for idx, id in enumerate(auctions_ids_list):
            buffer.append(id)

            # Enviar caso seja o último elemento.
            if idx == len(auctions_ids_list) - 1:
                data = self.parse_data_update(buffer)
                response = wuzu_service.call_wuzu(endpoint="/auction/update_many", data=data)

            # Enviar caso o buffer esteja cheio.
            if len(buffer) == 20:
                data = self.parse_data_update(buffer)
                response = wuzu_service.call_wuzu(endpoint="/auction/update_many", data=data)

    def send_open(self, wallet_id, schedule_id):
        wuzu_service = WuzuService()
        data = self.parse_data_open(wallet_id, schedule_id)
        response = wuzu_service.call_wuzu(endpoint="/auction/send_many", data=data)

    # ------------------------------------------------------------------------------------------

    def parse_data_open(self, wallet_id, schedule_id):
        return {"start_time": self.start_time, "end_time": self.end_time,
                "schedule_id": schedule_id,"wallet_id": wallet_id}

    def parse_data_update(self, buffer):
        return {"auction_ids": buffer, "body": {"start_time": self.start_time, "end_time": self.end_time}}

    def set_times(self, properties, task_requests) -> None:
        is_prod = os.environ.get("STAGE")
        gmt_hours = 5 if is_prod == "PROD" else 3

        self.start_time = (task_requests.get('data_inicio') -timedelta(hours=gmt_hours)).strftime("%Y-%m-%d %H:%M")
        self.end_time = (properties[0].data_limite - timedelta(hours=gmt_hours)).strftime("%Y-%m-%d %H:%M")
