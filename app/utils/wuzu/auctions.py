import os
from datetime import timedelta, datetime
from utils.wuzu.service import WuzuService
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.task_control.progressbar import TaskProgress


class Auctions:

    def __init__(self) -> None:
        self.start_time = None
        self.end_time = None
        self.wallet_id = None
        self.schedule_id = None

    def handle_auctions(self, task_requests):
        self.wallet_id = task_requests.get("id_obj")

        properties = PropertyRepository().get_properties_wallet_to_wuzu(self.wallet_id)

        """
        Explicação de: total=int( (len(properties)/5) *2) +7)

        - Divido por 5, pois atualizamos de 5 em 5 imóveis a porcentagem da Task.
        - Vezes 2, pois rodamos tanto aqui para a Wuzu, como para o Certificado de Venda, por Imóvel.
        - +5, são passos a mais que existem dentro da geração dos Contratos. Sendo 7 no Regulamento.
        """
        TaskProgress.update_task_progress(total=int((len(properties)/5) *2) + 7)
        print(f"Total tasks: {int((len(properties)/5) *2) + 10}")

        self.schedule_id = properties[0].schedule_id if len(properties) > 0 else ""
        type_vault = properties[0].tipo_cofre
        self._set_times(task_requests)

        properties_with_auction = self._get_and_validate_properties_auction(properties=properties)
        properties_without_auction = [p for p in properties if p.wuzu_disputa_id == None]

        print(f"properties_with_auction: {len(properties_with_auction)}")
        print(f"properties_without_auction: {len(properties_without_auction)}")

        # Imóveis COM Disputa aberta.
        if len(properties_with_auction) > 0:
            self.send_wuzu(properties_with_auction, "update", type_vault)

        # Imóveis SEM Disputa aberta.
        if len(properties_without_auction) > 0:
            self.send_wuzu(properties_without_auction, "send", type_vault)

        # Validação se algum imóvel ficou sem auction.
        self.validate_auctions(properties)

    # ------------------------------------------------------------------------------------------

    def send_wuzu(self, ids, action, type_vault):
        type_vault
        wuzu_service = WuzuService(type_vault)

        for idx, id in enumerate(ids):
            data = self._parse_data(id, action)
            print(f"Send Wuzu: {id} - {action}")
            response = wuzu_service.call_wuzu(endpoint=f"/auction/{action}", data=data)

            if idx % 5 == 0:
                print(f"Updated Task Progress p/ o idx {idx}")
                TaskProgress.update_task_progress()

    # ------------------------------------------------------------------------------------------

    @staticmethod
    def validate_auctions(properties):
        properties_tuple = tuple([imovel.imovel_id for imovel in properties])
        auctions_ids = PropertyAuctionRepository().get_wuzu_auction_id_by_many_properties(
            properties_tuple, properties[0].schedule_id)

        if len(properties) != len(auctions_ids):
            raise Exception(f"Problema na geração de Auction da wuzu.\nDos {len(properties)} imóveis \
                            apenas {len(auctions_ids)} tiveram Auction gerada.")

    def _parse_data(self, buffer, action):
        if action == "update":
            return self.__parse_data_update(buffer)

        return self.__parse_data_open(buffer)

    def __parse_data_open(self, buffer):
        return {"name": f"{buffer.codigo} - {buffer.idr} - {datetime.now().strftime('%Y%m%d%H%M%S')}",
                "start_time": self.start_time, "end_time": self.end_time,
                "schedule_id": self.schedule_id, "property_id": buffer.imovel_id}

    def __parse_data_update(self, buffer):
        return {"auction_id": buffer.wuzu_disputa_id, "body": {"start_time": self.start_time, "end_time": self.end_time},
                "property_id": buffer.imovel_id}

    def _set_times(self, task_requests) -> None:
        is_prod = os.environ.get("STAGE").upper()
        gmt_hours = 5 if is_prod == "PROD" else 3

        self.start_time = (task_requests.get('data_inicio') + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
        self.end_time = (task_requests.get("data_fim") + timedelta(hours=gmt_hours)).strftime("%Y-%m-%d %H:%M")

    def _get_and_validate_properties_auction(self, properties):
        properties_with_auction = [p for p in properties if p.wuzu_disputa_id != None]

        for p in properties_with_auction.copy():
            # Verificação para saber se a data que está vindo no Payload é a mesma que já está na tabela DisputaWuzu.
            same_date = (self.start_time == p.data_inicio_disputa.strftime("%Y-%m-%d %H:%M")) \
                            and (self.end_time == p.data_final_disputa.strftime("%Y-%m-%d %H:%M"))

            if same_date:
                properties_with_auction.remove(p)

        return properties_with_auction