from app.api.contract.contract_builder_base import ContractBuilderBase
from app.api.common.repositories.wallet_repository import WalletRepository
from app.api.common.repositories.seller_repository import SellerRepository
from app.api.common.repositories.qualification_repository import QualificationRepository
from app.api.common.repositories.property_auction_repository import PropertyAuctionRepository
from app.api.contract.regulamento_concorrencia.regulamento_helpers import set_property_valor
from app.api.contract.regulamento_concorrencia.regulamento_facade import RegulamentoConcorrenciaFacade
from app.api.contract.regulamento_concorrencia.regulamento_factory import RegulamentoDocumentsFactory


class RegulamentoConcorrenciaBuilder(ContractBuilderBase):

    def __init__(self, data) -> None:
        super().__init__()
        if not "wallet_id" in data:
            raise Exception("[ERROR]: Missing wallet_id")
        self.wallet_id = data.get("wallet_id")


    def build(self):
        data = self.get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)
        self._generate_documents(documents_objects)

        return ""


    def __get_documents_objects_list(self, data):
        regulamento_documents_factory = RegulamentoDocumentsFactory().get_instance(self.wallet_id, data)

        return regulamento_documents_factory

    def get_contract_data(self):
        # Arrumar um jeito de pegar Manager ID
        manager_id = '4dd4393a-2318-4576-8d8f-56b25c5c0e3a'

        wallet = WalletRepository().get_wallet_details(self.wallet_id)

        properties = WalletRepository().get_properties_wallet(self.wallet_id)
        properties = [set_property_valor(dict(property), self.wallet_id) for property in properties]
        properties = sorted(properties, key=lambda p: p['lote'] if p['lote'] else "", reverse=True)

        payment_methods = SellerRepository().get_payment_method(payment_form_id=wallet.forma_pagamento_id)
        qualification = QualificationRepository().fetch_qualifications_of_manager(manager=manager_id)

        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                p['installments_db'] = SellerRepository().get_payment_installments(p.get('id'))

        wuzu_action = PropertyAuctionRepository().get_wuzu_auction_id_by_property_id_from_property_auction(
            properties[0].get("imovel_id"), properties[0].get("schedule_id")
        )

        regulamento_facade = RegulamentoConcorrenciaFacade(
            wallet=wallet,
            payment_methods=payment_methods,
            properties=properties,
            wuzu_action=wuzu_action,
            qualificacao=qualification)

        return regulamento_facade.parse()
