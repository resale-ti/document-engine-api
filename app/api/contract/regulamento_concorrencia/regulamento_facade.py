import os
from api.common.helpers import number_format
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import date, timedelta

today = date.today()


class RegulamentoConcorrenciaFacade(ContractFacadeInterface):

    def __init__(self, wallet, payment_methods, properties, regulamento_dates, qualificacao):
        self.wallet = wallet
        self.payment_methods = payment_methods
        self.properties = properties
        self.qualificacao = qualificacao
        self.regulamento_dates = regulamento_dates

    def parse(self) -> dict:
        base_data = self._get_base_data()
        datas_concorrencia = self._get_datas_concorrencia()
        payment_methods = self._get_payment_methods()
        imoveis = self._get_imoveis_data()

        return dict(**base_data, **datas_concorrencia, **payment_methods, **imoveis)

    def _get_payment_methods(self):
        payment_methods = self.payment_methods
        payment_desc_vista = ""
        payment_desc_parcelado = ""

        for method in payment_methods:
            if method.get("tipo_condicao") == "vista":
                condicao_vista = "X"
                conector_v = "; " if payment_desc_vista else ""
                payment_desc_vista += conector_v + self._get_payment_desc_vista(method=method)
            elif method.get("tipo_condicao") == "parcelado":
                condicao_parcelado = "X"
                conector_p = "; " if payment_desc_parcelado else ""
                payment_desc_parcelado += conector_p + self._get_payment_desc_parcelado(method=method)
            else:
                pass

        return {
            "CONDICAO_VISTA": condicao_vista if 'condicao_vista' in locals() else "",
            "CONDICOES_PAGAMENTO_VISTA": payment_desc_vista,
            "CONDICAO_PARCELADO": condicao_parcelado if 'condicao_parcelado' in locals() else "",
            "CONDICOES_PAGAMENTO_PARCELADO": payment_desc_parcelado
        }

    def _get_payment_desc_parcelado(self, method):
        description = ""
        installments_db = method.get("installments_db")

        if not installments_db:
            return ""

        for installment in installments_db:
            conector = "; " if description else ""
            description += conector + f"{number_format(installment.get('porcentagem_entrada'), 0)}% de entrada e "

            if installment.get('qtd_fixa') > 0:
                description += f"saldo em até {installment.get('qtd_fixa')} parcelas"
            else:
                description += f"saldo em até {installment.get('qtd_maxima')} parcelas"

        return description

    def _get_payment_desc_vista(self, method):
        description = ""

        if int(method.get("porcentagem_sinal")) > 0:
            description = number_format(method.get("porcentagem_sinal"), 0) + "% de entrada"

        if int(method.get("porcentagem_ccv") > 0):
            ini_d = ", " if description else ""
            description += ini_d + number_format(method.get("porcentagem_ccv"), 0) + "% do pagamento na emissão do CCV (Contrato de Compra e Venda)"

        if int(method.get("porcentagem_escritura") > 0):
            ini_d = ", " if description else ""
            description += ini_d + number_format(method.get("porcentagem_escritura"), 0) + "% na escritura"

        if int(method.get("a_vista_desconto") > 0):
            ini_d = ", c/ " if description else "c/"
            description += ini_d + number_format(method.get("a_vista_desconto"), 0) + "% de desconto sobre o valor do lance vencedor"

        return description

    def _get_base_data(self) -> dict:
        return {
            "regulamento": self.wallet.modelo_regulamento if self.wallet.modelo_regulamento else "MLP_002",
            "N_REGULAMENTO": self.wallet.disputa_id,
            "QUALIFICACAO_VENDEDORES": self.qualificacao[0].conteudo if self.qualificacao else "",
            "PORTAL_VENDEDOR": self.properties[0].get("url_whitelabel"),
            "TAXA_SERVICO": round(self.wallet.tx_servico, 2) if self.wallet.tx_servico else 0,
            "TAXA_INTERMEDIACAO": round(self.wallet.tx_comissao, 2) if self.wallet.tx_comissao else 0,
            "DATA_ATUAL": today.strftime('%d/%m/%Y')
        }

    def _get_datas_concorrencia(self) -> dict:
        is_prod = os.environ.get("STAGE")
        gmt_hours = 5 if is_prod == "PROD" else 3

        data_inicio = self.regulamento_dates.get("data_inicio")
        data_fim = self.regulamento_dates.get("data_fim")

        return {
            "DATA_INICIO": (data_inicio - timedelta(hours=3)).strftime('%d/%m/%Y'),
            "HORA_INICIO": (data_inicio - timedelta(hours=3)).strftime('%H:%M'),
            "DATA_FIM": (data_fim - timedelta(hours=gmt_hours)).strftime('%d/%m/%Y'),
            "HORA_FIM": (data_fim - timedelta(hours=gmt_hours)).strftime('%H:%M'),
        }

    def _get_imoveis_data(self) -> list:
        return {"imoveis": list(map(self.parse_imoveis, self.properties))}

    @staticmethod
    def parse_imoveis(property_obj: dict) -> dict:
        lance_minimo = number_format(property_obj.get("valor_proposto")) if property_obj.get("valor_proposto") else "0,00"

        return {
            "LOTE" : property_obj.get("lote") if property_obj.get("lote") else "-",
            "ID_BANCO" : property_obj.get("id_no_banco"),
            "DESCRICAO_LEGAL" : property_obj.get("descricao_legal_description"),
            "CONSIDERACOES_IMPORTANTES" : property_obj.get("consideracoes_importantes"),
            "LANCE_MINIMO" : f"R$ {lance_minimo}"
        }
