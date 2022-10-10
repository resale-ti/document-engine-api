import os
from api.common.helpers import number_format
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import date, timedelta

today = date.today()


class RegulamentoConcorrenciaFacade(ContractFacadeInterface):

    def __init__(self, wallet, payment_methods, cronograma, properties, proponente, encarregado):
        self.wallet = wallet
        self.payment_methods = payment_methods
        self.properties = properties
        self.cronograma = cronograma
        self.proponente = proponente
        self.encarregado = encarregado

    def parse(self) -> dict:
        base_data = self.__get_base_data()
        payment_methods = self.__get_payment_methods()
        imoveis = self.__get_imoveis_data()

        return dict(**base_data, **payment_methods, **imoveis)

    def __get_imoveis_data(self):
        lista = []
        lista.append({
            'LOTE': "",
            'ID_BANCO': "",
            'PRIMEIRO_LEILAO_VALOR': "",
            'SEGUNDO_LEILAO_VALOR': "",
            'DESCRICAO_LEGAL': "",
            'VALOR_VENDA': "",
            'VALOR_PROPOSTO': "",
            'VALOR_MINIMO': "",
            'PGI_QUANTIDADE': "",
            'CONSIDERACOES_IMPORTANTES': ""
        })
        return {
            'imoveis': lista,
        }

    def __get_payment_methods(self):
        return {
            'in_cash_payment_desc': "",
            'installments_payment_desc': "",
            'condition_type_in_cash': "",
            'condition_type_installments': "",
            'cash_payment_text': "",
            'parceled_payment_text': "",
            'financing_payment_text': "",
            'condition_type_financiado': ""
        }

    def __get_base_data(self) -> dict:
        return {
            "CARTEIRA_ID": "",
            'MODELO_EDITAL': "",
            'DATA_LIMITE': "",
            'PRIMEIRO_LEILAO_DATA': "",
            'SEGUNDO_LEILAO_DATA': "",
            'PRIMEIRO_LEILAO_VALOR': "",
            'SEGUNDO_LEILAO_VALOR': "",
            'CANAL_VENDA_NOME': "",
            'NUMERO_LEILAO': "",
            'ENCARREGADO': "",
            'DATA': "",
            'HORA': "",
            'SITE': "",
            'NOME_LEILOEIRO_OFICIAL': "",
            'CPF_CNPJ': "",
            'UF_JUCESP': "",
            'NUMERO_JUCESP': "",
            'RESPONSAVEL_NOME': "",
            'SIGNATARIO': "",
            'RESPONSAVEL_CPF': "",
            'RESPONSAVEL_TELEFONE': "",
            'RESPONSAVEL_EMAIL': "",
            'ENDERECO_LOGRADOURO': "",
            'ENDERECO_COMPLEMENTO': "",
            'ENDERECO_CIDADE': "",
            'ENDERECO_UF': "",
            'ENDERECO_CEP': "",
            'PAGAMENTO_DINHEIRO': "",
            'PAGAMENTO_DINHEIRO_TEXTO': "",
            'PAGAMENTO_CONDICAO_TIPO': "",
            'PAGAMENTO_DINHEIRO_CONDICAO': "",
            'PAGAMENTO_PARCELADO_CONDICAO': "",
            'PAGAMENTO_PARCELADO_TEXTO': "",
            'PAGAMENTO_FINANCIADO_TEXTO': "",
            'PAGAMENTO_FINANCIADO_CONDICAO': "",
            'DIA_CORRENTE': "",
            'MES_CORRENTE': "",
            'ANO_CORRENTE': "",
            'TAXA_PAGIMOVEL': "",
            'DADOS_BANCO_VENDEDORES': "",
            'DADOS_QUALIFICACAO_VENDEDORES': "",
        }

    @staticmethod
    def __get_imoveis_data(property: dict) -> dict:
        return {
            "LOTE": property.get("lote") if property.get("lote") else "-",
            "ID_BANCO": property.get("id_no_banco"),
            "DESCRICAO_LEGAL": property.get("descricao_legal_description"),
            "CONSIDERACOES_IMPORTANTES": property.get("consideracoes_importantes"),
            "LANCE_MINIMO": f"R$ {lance_minimo}"
        }
