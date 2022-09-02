import os
from api.common.helpers import float_format_str
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import date, timedelta

today = date.today()


class RegulamentoConcorrenciaFacade(ContractFacadeInterface):

    def __init__(self, wallet, payment_methods, properties, wuzu_action, qualificacao):
        self.wallet = wallet
        self.payment_methods = payment_methods
        self.properties = properties
        self.wuzu_action = wuzu_action
        self.qualificacao = qualificacao

    def parse(self) -> dict:
        base_data = self.__get_base_data()
        datas_concorrencia = self.__get_datas_concorrencia()
        # payment_methods = self.__get_payment_methods()
        imoveis = self.__get_imoveis_data()

        return ""

    def __get_payment_methods(self):
        pass

    def __get_base_data(self) -> dict:
        return {
            "regulamento": self.wallet.modelo_regulamento if self.wallet.modelo_regulamento else "CPBB001_001",
            "N_REGULAMENTO": self.wallet.disputa_id,
            "QUALIFICACAO_VENDEDORES": self.qualificacao[0].conteudo if self.qualificacao else "",
            "PORTAL_VENDEDOR": self.properties[0].get("url_whitelabel"),
            "TAXA_SERVICO": round(self.wallet.tx_servico, 2) if self.wallet.tx_servico else 0,
            "TAXA_INTERMEDIACAO": round(self.wallet.tx_comissao, 2) if self.wallet.tx_comissao else 0,
            "DATA_ATUAL": today.strftime('%d/%m/%Y')
        }

    def __get_datas_concorrencia(self) -> dict:
        if self.wuzu_action:
            is_prod = os.environ.get("STAGE")
            gmt_hours = 5 if is_prod == "PROD" else 3

            data_inicio = self.wuzu_action.date_start_auction
            data_fim = self.wuzu_action.date_finish_auction

            return {
                "DATA_INICIO": (data_inicio - timedelta(gmt_hours)).strftime('%d/%m/%Y'),
                "HORA_INICIO": (data_inicio - timedelta(gmt_hours)).strftime('%H:%m'),
                "DATA_FIM": (data_fim - timedelta(gmt_hours)).strftime('%d/%m/%Y'),
                "HORA_FIM": (data_fim - timedelta(gmt_hours)).strftime('%H:%m'),
            }
        else:
            return {
                "DATA_INICIO": "",
                "HORA_INICIO": "",
                "DATA_FIM": "",
                "HORA_FIM": "",
            }

    def __get_imoveis_data(self) -> list:
        return list(map(self.parse_imoveis, self.properties))

    @staticmethod
    def parse_imoveis(property: dict) -> dict:
        lance_minimo = float_format_str(property.get("valor_proposto")) if property.get("valor_proposto") else "0,00"

        return {
            "LOTE" : property.get("lote") if property.get("lote") else "-",
            "ID_BANCO" : property.get("id_no_banco"),
            "DESCRICAO_LEGAL" : property.get("descricao_legal_description"),
            "CONSIDERACOES_IMPORTANTES" : property.get("consideracoes_importantes"),
            "LANCE_MINIMO" : f"R$ {lance_minimo}"
        }
