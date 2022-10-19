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
from datetime import datetime
from api.common.helpers import parse_to_money


class CertificadoVendaBuilder(ContractBuilderBase):

    contract_base_name = "CertificadoVenda"
    stylesheet_path = "static/contracts_templates/certificado_venda/default-style.css"
    pagination = False

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.wallet_id = data.get("id_obj")
        self.property_id = data.get("property_id")

    def build(self) -> None:
        wallet, property, key = self._generate_property_sale_certificate()

        data = self.__get_data(wallet, property, key)

        documents_objects = self.__get_documents_objects_list(data)

        self._generate_documents(documents_objects)

    def _generate_property_sale_certificate(self):

        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        if len(wallet) == 0:
            raise Exception("[ERROR]: Missing wallet_id")

        property = PropertyRepository().get_properties_detail_by_wallet(
            imovel_id=self.property_id, wallet_id=self.wallet_id)

        if len(property) == 0:
            raise Exception("Imóvel não encontrado")

        key = CertificadoVendaLibrary.generate_new_key(wallet=wallet)

        self._generate_property_log(wallet, property)

        return wallet, property, key

    def __get_documents_objects_list(self, data):
        return [CertificadoVendaCapa(self.wallet_id, data),
                CertificadoVendaRegulamentoAprovado(data.get('regulamento_url')),
                CertificadoVendaLogsLayer(self.wallet_id, data)]

    def __get_data(self, wallet, property, key):

        schedule = SchedulesRepository().get_cronograma_carteira(self.wallet_id)

        regulamento_db = DocumentRepository().get_wallet_regulamento(self.wallet_id)

        last_regulamento = []

        for r in regulamento_db:
            if r.documento_status == 'approved' or r.documento_status == 'pending' and r.data > regulamento_data:
                regulamento_data = r.data_criacao
                last_regulamento = r

        logs = SalesCertificateRepository().get_log(self.wallet_id, self.property_id)

        sale_certificate_number = key

        certificado_venda_facade = CertificadoVendaFacade(
            wallet,
            schedule,
            property,
            last_regulamento,
            logs,
            sale_certificate_number
        )

        return certificado_venda_facade.parse()

    def _generate_property_log(self, wallet, property):
        # values = get_property_valor_venda(property_id=property.imovel_id, wallet_id=wallet.id)
        values = {"valor_avaliacao": 10000.32, "valor_venda": 30000.54}

        valor_avaliado = values.get("valor_avaliacao")
        valor_venda = values.get("valor_venda")

        condicoes_pagamento_texto = CarteirasIntegration().get_condicoes_pagamentos(property.imovel_id)

        numero_grupo = property.lote

        schedule = SchedulesRepository().get_cronograma_carteira(self.wallet_id)

        """
         * Imóvel publicado com Valor avaliado R$ X, valor do imóvel R$ X,
         * data da concorrência X, condições de pagamento X, número do grupo X, cronograma X,
         * status da venda X, % comissão, % taxa pgi, % taxa gerenciamento
         */
        """
        data_mp = property.data_limite.strftime("%d/%m/%Y")
        hora_mp = property.data_limite.strftime("%H:%m")

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
            + ", taxa gerenciamento " + str(float(wallet.tx_gerenciamento)) + "%."

        # // Snapshot
        data = {"data_criacao": datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
                "carteira_id": wallet.id,
                "imovel_id": property.imovel_id,
                "descricao": description}

        SalesCertificateRepository().add_log(data)

