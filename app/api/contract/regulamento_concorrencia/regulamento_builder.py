from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.seller_repository import SellerRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.contract.regulamento_concorrencia.regulamento_helpers import set_property_valor
from api.contract.regulamento_concorrencia.regulamento_facade import RegulamentoConcorrenciaFacade
from api.contract.regulamento_concorrencia.regulamento_factory import RegulamentoDocumentsFactory
from utils.admin_integrations.documents import AdminAPIDocuments
from datetime import date


class RegulamentoConcorrenciaBuilder(ContractBuilderBase):

    doc_name = "Regulamento Concorrencia"

    def __init__(self, data) -> None:
        super().__init__()

        if not "id" in data:
            raise Exception("[ERROR]: Missing wallet_id")

        self.wallet_id = data.get("id_obj")
        self.manager = ()

    def build(self) -> None:
        data = self.__get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)
        file_bytes_b64 = self._generate_documents(documents_objects)

        data_admin = self.mount_data_admin_document(file_bytes_b64=file_bytes_b64)

        response = AdminAPIDocuments().post_create_document(data=data_admin)


    def mount_data_admin_document(self, file_bytes_b64):
        doc_name = f"{self.doc_name} - {self.manager.nome} - {date.today().strftime('%Y%m%d')}.pdf"

        return {
            "nome_doc": doc_name,
            "documento_nome": doc_name,
            "categoria_id": "regulamento",
            "file_mime_type": "application/pdf",
            "file": file_bytes_b64.decode('utf-8'),
            "documento_status": "approved"
        }

    def __get_documents_objects_list(self, data):
        regulamento_documents_factory = RegulamentoDocumentsFactory(
        ).get_instance(self.wallet_id, data)

        return regulamento_documents_factory

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)

        wallet = WalletRepository().get_wallet_details(self.wallet_id)

        properties = WalletRepository().get_properties_wallet(self.wallet_id)
        properties = [set_property_valor(
            dict(property), self.wallet_id) for property in properties]
        properties = sorted(
            properties, key=lambda p: p['lote'] if p['lote'] else "", reverse=True)

        payment_methods = SellerRepository().get_payment_method(
            payment_form_id=wallet.forma_pagamento_id)
        qualification = QualificationRepository(
        ).fetch_qualifications_of_manager(manager=self.manager.id)

        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                p['installments_db'] = SellerRepository(
                ).get_payment_installments(p.get('id'))

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
