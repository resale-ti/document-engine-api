from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.seller_repository import SellerRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.contract.edital.edital_helpers import set_property_valor
from api.contract.edital.edital_facade import EditalFacade
from api.contract.edital.edital_factory import EditalFactory
from api.contract.edital.edital_library import EditalLibrary
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.wallets import AdminAPIWallets
from api.common.helpers import update_task_progress
import time
from datetime import date


class EditalBuilder(ContractBuilderBase):

    doc_name = "Edital"

    def __init__(self, data: dict) -> None:
        super().__init__()

        if not "id_obj" in data:
            raise Exception("[ERROR]: Missing wallet_id")

        self.wallet_id = data.get("id_obj")
        self.manager = ()
        self.requester_id = data.get("requester_id")
        self.data_inicio_regulamento = data.get("data_inicio")

    def build(self) -> None:
        #update_task_progress(current=1, total=5)
        data = self.__get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)

        #update_task_progress(current=2, total=5)
        file_bytes_b64 = self._generate_documents(documents_objects)

        #update_task_progress(current=3, total=5)
        doc_data = self._handle_with_admin(file_bytes_b64=file_bytes_b64)
        document_id = doc_data.get("document_id")

        #update_task_progress(current=4, total=5)
        #RegulamentoConcorrenciaLibrary().inactive_documents_from_wallet_id(
        #    wallet_id=self.wallet_id, document_id=document_id)

        #RegulamentoConcorrenciaLibrary().send_approved_document_email(self.wallet_id, document_id, file_bytes_b64)
        #update_task_progress(current=5, total=5)


    def _handle_with_admin(self, file_bytes_b64):
        doc_data = self.mount_data_admin_document(
            file_bytes_b64=file_bytes_b64)

        response = AdminAPIDocuments().post_create_document(data=doc_data)

        document_id = response.get("id")

        AdminAPIWallets().post_create_wallet_related_document(
            wallet_id=self.wallet_id, body={"data": [document_id]})

        doc_data["document_id"] = document_id

        return doc_data

    def mount_data_admin_document(self, file_bytes_b64):
        doc_name = f"{self.doc_name} - {self.manager.nome} - {date.today().strftime('%Y%m%d')}"

        return {
            "nome_doc": doc_name,
            "documento_nome": doc_name + ".pdf",
            "categoria_id": "regulamento",
            "file_mime_type": "application/pdf",
            "file": file_bytes_b64.decode('utf-8'),
            "tipo_exibicao": "publico",
            "usuario_responsavel_id": self.requester_id,
            "documento_status": "approved"
        }

    def __get_documents_objects_list(self, data):
        regulamento_documents_factory = EditalFactory(
        ).get_instance(self.wallet_id, data)

        return regulamento_documents_factory

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)

        wallet = WalletRepository().get_wallet_details(self.wallet_id)

        properties = PropertyRepository().get_properties_wallet(self.wallet_id)
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

        regulamento_dates = {"data_inicio": self.data_inicio_regulamento,
                             "data_fim": properties[0].get("data_limite")}

        edital_facade = EditalFacade(
            wallet=wallet,
            payment_methods=payment_methods,
            properties=properties,
            regulamento_dates=regulamento_dates,
            qualificacao=qualification)

        return edital_facade.parse()
