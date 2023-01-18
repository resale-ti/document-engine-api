import os
from api.common.helpers import number_format
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import date, timedelta

today = date.today()


class EditalFacade(ContractFacadeInterface):

    def __init__(self, wallet, payment_methods, cronograma, properties, proponente, aux, manager_responsible):
        self.wallet = wallet
        self.payment_methods = payment_methods
        self.properties = properties
        self.cronograma = cronograma
        self.proponente = proponente
        self.aux = aux
        self.manager_responsible = manager_responsible

    def parse(self) -> dict:
        base_data = self.__get_base_data()
        imoveis = self.__get_imoveis_data()

        return dict(**base_data, **imoveis)

    def __get_base_data(self) -> dict:
        return {
            "CARTEIRA_ID": self.wallet.id,
            'DATA_LIMITE': self.properties[0].data_limite,
            'PRIMEIRO_LEILAO_DATA': self.properties[0].data_primeiro_leilao_data,
            'SEGUNDO_LEILAO_DATA': self.properties[0].data_segundo_leilao_data,
            'PRIMEIRO_LEILAO_VALOR': self.properties[0].valor_primeiro_leilao_valor,
            'SEGUNDO_LEILAO_VALOR': self.properties[0].valor_segundo_leilao_valor,
            'CANAL_VENDA_NOME': self.cronograma.canal_venda_id,
            'NUMERO_LEILAO': self.wallet.numero_leilao,
            'DATA': date(),
            'HORA': date(),
            'SITE': self.cronograma.site,
            'NOME_LEILOEIRO_OFICIAL': self.cronograma.responsavel_nome,
            'CPF_CNPJ': self.cronograma.responsavel_cpf,
            'UF_JUCESP': self.cronograma.uf_jucesp,
            'NUMERO_JUCESP': self.cronograma.numero_jucesp,
            'RESPONSAVEL_NOME': self.proponente.primeiro_nome + self.proponente.ultimo_nome if self.proponente else "",
            'SIGNATARIO': self.proponente.primeiro_nome + self.proponente.ultimo_nome if self.proponente else self.cronograma.responsavel_nome,
            'RESPONSAVEL_CPF': self.proponente.primeiro_nome + self.proponente.ultimo_nome if self.proponente else "",
            'RESPONSAVEL_TELEFONE': self.proponente.primeiro_nome + self.proponente.ultimo_nome if self.proponente else self.cronograma.canal_responsavel_telefone,
            'RESPONSAVEL_EMAIL': self.proponente.primeiro_nome + self.proponente.ultimo_nome if self.proponente else self.cronograma.responsavel_email,
            'ENDERECO_LOGRADOURO': self.cronograma.endereco_rua + ', ' + self.cronograma.endereco_numero + ', ' + self.cronograma.endereco_bairro,
            'ENDERECO_COMPLEMENTO': "",
            'ENDERECO_CIDADE': self.cronograma.endereco_cidade + '/' + self.cronograma.endereco_estado,
            'ENDERECO_CEP': self.cronograma.endereco_cep,
            'PAGAMENTO_DINHEIRO': "condition_type_in_cash",
            'PAGAMENTO_DINHEIRO_TEXTO': "cash_payment_text",
            'PAGAMENTO_CONDICAO_TIPO': "payment_conditions_installments",
            'PAGAMENTO_DINHEIRO_CONDICAO': "payment_conditions_cash",
            'PAGAMENTO_PARCELADO_CONDICAO': " installments_payment",
            'PAGAMENTO_PARCELADO_TEXTO': "parceled_payment_text",
            'PAGAMENTO_FINANCIADO_TEXTO': "condition_type_financiado",
            'PAGAMENTO_FINANCIADO_CONDICAO': "financing_payment_text",
            'DIA_CORRENTE': date("d"),
            'MES_CORRENTE': date("m"),
            'ANO_CORRENTE': date("Y"),
            'TAXA_PAGIMOVEL': round(self.wallet.tx_servico, 2) if self.wallet.tx_servico else 0,
            'TAXA_MINIMA': 0,
        }

    @staticmethod
    def __get_imoveis_data(property: dict) -> dict:
        return {
            "LOTE": property.get("lote") if property.get("lote") else "-",
            "ID_BANCO": property.get("id_banco"),
            "DESCRICAO_LEGAL": property.get("legal_description"),
            "CONSIDERACOES_IMPORTANTES": property.get("consideracoes_importantes"),
            "LANCE_MINIMO": f"R$ {property.get('valor_venda')}"
        }
        
        
