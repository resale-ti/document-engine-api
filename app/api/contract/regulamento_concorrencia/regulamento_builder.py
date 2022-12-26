import os

from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.payment_repository import PaymentRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.contract.regulamento_concorrencia.regulamento_helpers import set_property_valor
from api.contract.regulamento_concorrencia.regulamento_facade import RegulamentoConcorrenciaFacade
from api.contract.regulamento_concorrencia.regulamento_factory import RegulamentoDocumentsFactory
from api.contract.regulamento_concorrencia.regulamento_library import RegulamentoConcorrenciaLibrary
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.wallets import AdminAPIWallets
from api.task_control.progressbar import TaskProgress
from datetime import date


class RegulamentoConcorrenciaBuilder(ContractBuilderBase):

    doc_name = "Regulamento Concorrencia"

    def __init__(self, data: dict) -> None:
        super().__init__()

        if not "id_obj" in data:
            raise Exception("[ERROR]: Missing wallet_id")

        self.wallet_id = data.get("id_obj")
        self.manager = ()
        self.requester_id = data.get("requester_id")
        self.data_inicio_regulamento = data.get("data_inicio")
        self.data_fim_regulamento = data.get("data_fim")

    def build(self) -> None:
        TaskProgress.update_task_progress()
        data = self.__get_contract_data()
        documents_objects = self.__get_documents_objects_list(data)

        TaskProgress.update_task_progress()
        file_bytes_b64 = self._generate_documents(documents_objects)

        TaskProgress.update_task_progress()
        doc_data = self._handle_with_admin(file_bytes_b64=file_bytes_b64)
        document_id = doc_data.get("document_id")

        TaskProgress.update_task_progress()
        RegulamentoConcorrenciaLibrary().inactive_documents_from_wallet_id(
            wallet_id=self.wallet_id, document_id=document_id)

        RegulamentoConcorrenciaLibrary().send_approved_document_email(self.wallet_id,
                                                                      document_id,
                                                                      file_bytes_b64)
        TaskProgress.update_task_progress()

    def _handle_with_admin(self, file_bytes_b64):
        doc_data = self.mount_data_admin_document(
            file_bytes_b64=file_bytes_b64)

        response = AdminAPIDocuments().post_create_document(data=doc_data)

        document_id = response.get("id")

        os.environ["DOCUMENT_ID_RC"] = document_id

        response_wallet = AdminAPIWallets().post_create_wallet_related_document(
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
        regulamento_documents_factory = RegulamentoDocumentsFactory(
        ).get_instance(self.wallet_id, data)

        return regulamento_documents_factory

    def __get_contract_data(self):
        self.manager = ManagerRepository().get_manager_by_wallet_id(self.wallet_id)

        wallet = WalletRepository().get_wallet_details(self.wallet_id)

        properties = PropertyRepository().get_properties_wallet_with_schedule(self.wallet_id)

        if not properties:
            raise Exception(f"Não foi encontrado imóvel com Disputa para a carteira com ID: {self.wallet_id}")

        properties = [set_property_valor(dict(property_obj), self.wallet_id) for property_obj in properties]
        properties = sorted(properties, key=lambda p: int(p['lote']) if p['lote'] else "")

        payment_methods = PaymentRepository().get_payment_method(payment_form_id=wallet.forma_pagamento_id)
        qualification = QualificationRepository().fetch_qualifications_of_manager(manager=self.manager.id)

        for p in payment_methods:
            if (p.get('tipo_condicao') == 'parcelado'):
                p['installments_db'] = PaymentRepository(
                ).get_payment_installments(p.get('id'))

        regulamento_dates = {"data_inicio": self.data_inicio_regulamento,
                             "data_fim": self.data_fim_regulamento}

        regulamento_facade = RegulamentoConcorrenciaFacade(
            wallet=wallet,
            payment_methods=payment_methods,
            properties=properties,
            regulamento_dates=regulamento_dates,
            qualificacao=qualification)

        return regulamento_facade.parse()
