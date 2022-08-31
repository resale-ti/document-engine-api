from app.api.contract.contract_builder_interface import ContractBuilderInterface
from app.api.contract.contract_builder_base import ContractBuilderBase
from app.api.common.repositories.wallet_repository import WalletRepository
from app.api.common.repositories.seller_repository import SellerRepository
from app.api.common.repositories.qualification_repository import QualificationRepository
from app.api.common.repositories.property_auction_repository import PropertyAuctionRepository
from app.api.contract.regulamento_concorrencia.regulamento_helpers import set_property_valor


class RegulamentoConcorrenciaBuilder(ContractBuilderBase, ContractBuilderInterface):

    _document_id = None
    _contract_base_name = "RegulamentoConcorrencia"
    _stylesheet_path = "static/templates/regulamento_concorrencia/regulamento.css"
    _header_logo = False

    def __init__(self, data) -> None:
        if not "wallet_id" in data:
            raise Exception("[ERROR]: Missing wallet_id")
        self.wallet_id = data.get("wallet_id")


    def build(self):
        data = self.get_contract_data()

    def get_file_name(self):
        """Isso aqui provavelmente não vai ser desse jeito."""
        pass

    def get_contract_data(self):
        # Arrumar um jeito de pegar Manager ID
        manager_id = '4dd4393a-2318-4576-8d8f-56b25c5c0e3a'

        wallet = WalletRepository().get_wallet_details(self.wallet_id)

        properties = WalletRepository().get_properties_wallet(self.wallet_id)
        properties = [set_property_valor(dict(property), self.wallet_id) for property in properties]
        properties = sorted(properties, key=lambda p: p['lote'], reverse=True)

        payment_methods = SellerRepository().get_payment_method(payment_form_id=wallet.forma_pagamento_id)
        qualification = QualificationRepository().fetch_qualifications_of_manager(manager=manager_id)

        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                p['installments_db'] = SellerRepository().get_payment_installments(p.get('id'))

        wuzu_action = PropertyAuctionRepository().get_wuzu_auction_id_by_property_id_from_property_auction(
            properties[0].get("imovel_id"), properties[0].get("schedule_id")
        )

        return payment_methods

    def __get_documents_objects_list(self):
        pass