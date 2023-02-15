from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.document_repository import DocumentRepository
from api.common.repositories.schedules_repository import SchedulesRepository
from api.common.repositories.sales_certificate_repository import SalesCertificateRepository
from api.contract.certificado_venda.certificado_library import CertificadoVendaLibrary
from api.contract.certificado_venda.certificado_facade import CertificadoVendaFacade
from api.contract.certificado_venda.certificado_layers import CertificadoVendaCapa, CertificadoVendaRegulamentoAprovado, CertificadoVendaLogsLayer
from utils.carteiras_integrations.carteiras_integrations import CarteirasIntegration
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.property import AdminAPIProperty
from api.task_control.progressbar import TaskProgress
from datetime import datetime, date
from api.common.helpers import get_property_valor_venda, parse_to_money


class CertificadoVendaBuilder(ContractBuilderBase):

    doc_name = "Certificado Venda"

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.wallet_id = data.get("id_obj")
        self.property_id = data.get("property_id")

    def build(self) -> None:
        wallet, property_obj, key = self._generate_property_sale_certificate()

        data = self.__get_data(wallet, property_obj, key)

        documents_objects = self.__get_documents_objects_list(data)

        file_bytes_b64 = self._generate_documents(documents_objects)

        self._handle_with_admin(file_bytes_b64, wallet, key)

    def _generate_property_sale_certificate(self):

        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        if len(wallet) == 0:
            raise Exception("[ERROR]: Missing wallet_id")

        property_obj = PropertyRepository().get_property_detail_by_wallet(
            imovel_id=self.property_id, wallet_id=self.wallet_id)

        if len(property_obj) == 0:
            raise Exception("Imóvel não encontrado")

        key = CertificadoVendaLibrary.generate_new_key(wallet=wallet)

        self._generate_property_log(wallet, property_obj)

        return wallet, property_obj, key

    def _handle_with_admin(self, file_bytes_b64, wallet, key):
        doc_data = self.__mount_data_admin_document(
            file_bytes_b64=file_bytes_b64, wallet=wallet, certificado_venda=key)

        response = AdminAPIDocuments().post_create_document(data=doc_data)

        document_id = response.get("id")

        AdminAPIProperty().post_create_property_related_document(
            property_id=self.property_id, body={"data": [document_id]})

    #####################################################################################
    # ------------------------ Utilites Functions  -------------------------------------#

    def __mount_data_admin_document(self, file_bytes_b64, wallet, certificado_venda):
        doc_name = f"{self.doc_name} - {wallet.codigo} - {certificado_venda} - {date.today().strftime('%Y%m%d')}"

        return {
            "nome_doc": doc_name,
            "documento_nome": doc_name + ".pdf",
            "categoria_id": "certificado_venda",
            "file_mime_type": "application/pdf",
            "file": file_bytes_b64.decode('utf-8'),
            "tipo_exibicao": "interno",
            "numero_certificado_venda": certificado_venda
        }

    def __get_documents_objects_list(self, data):
        return [CertificadoVendaCapa(self.wallet_id, data),
                CertificadoVendaRegulamentoAprovado(
                    data.get('regulamento_url')),
                CertificadoVendaLogsLayer(self.wallet_id, data)]

    def __get_data(self, wallet, property_obj, key):

        schedule = SchedulesRepository().get_cronograma_carteira(self.wallet_id)

        regulamento_db = DocumentRepository().get_active_regulamento_wallet(self.wallet_id)

        logs = SalesCertificateRepository().get_log(self.wallet_id, self.property_id)

        certificado_venda_facade = CertificadoVendaFacade(
            wallet, schedule, property_obj, regulamento_db, logs, key
        )

        return certificado_venda_facade.parse()

    def _generate_property_log(self, wallet, property_obj):
        values = get_property_valor_venda(property_id=property_obj.imovel_id, wallet_id=wallet.id)

        valor_avaliado = values.get("valor_avaliacao")
        valor_venda = values.get("valor_venda")

        condicoes_pagamento_texto = CarteirasIntegration(
        ).get_condicoes_pagamentos(property_obj.imovel_id)

        numero_grupo = property_obj.lote

        schedule = SchedulesRepository().get_cronograma_carteira(self.wallet_id)

        """
         * Imóvel publicado com Valor avaliado R$ X, valor do imóvel R$ X,
         * data da concorrência X, condições de pagamento X, número do grupo X, cronograma X,
         * status da venda X, % comissão, % taxa pgi, % taxa gerenciamento
         */
        """
        data_mp = property_obj.data_limite.strftime("%d/%m/%Y")
        hora_mp = property_obj.data_limite.strftime("%H:%m")

        schedule_data_inicio = schedule.data_inicio.strftime("%d/%m/%Y")
        schedule_data_final = schedule.data_final.strftime("%d/%m/%Y")

        description = "Imóvel publicado com valor avaliado R$ " + parse_to_money(valor_avaliado) \
            + ", valor do imóvel R$ " + parse_to_money(valor_venda) \
            + ", data da melhor proposta " + data_mp \
            + " às " + hora_mp \
            + ", condições de pagamento: " + condicoes_pagamento_texto \
            + ", número do grupo " + numero_grupo \
            + ", cronograma vigente de " + schedule_data_inicio + " até " + schedule_data_final \
            + ", status da venda " + wallet.status \
            + ", comissão " + str(float(wallet.tx_comissao)) + "%" \
            + ", taxa de serviço " + str(float(wallet.tx_servico)) + "%" \
            + ", taxa gerenciamento " + \
            str(float(wallet.tx_gerenciamento)) + "%."

        # // Snapshot
        data = {"data_criacao": datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
                "carteira_id": wallet.id,
                "imovel_id": property_obj.imovel_id,
                "descricao": description}

        SalesCertificateRepository().add_log(data)
