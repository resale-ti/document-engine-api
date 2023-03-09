from api.common.helpers import get_property_valor_venda, get_property_considerations_full
from api.contract.edital.edital_helpers import number_format_money
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import datetime


class EditalFacade(ContractFacadeInterface):

    def __init__(self, wallet, payment_methods, cronograma, properties, proponente, text_payments, manager_responsible):
        self.wallet = wallet
        self.payment_methods = payment_methods
        self.properties = properties
        self.cronograma = cronograma
        self.proponente = proponente
        self.text_payments = text_payments
        self.manager_responsible = manager_responsible

    def parse(self) -> dict:
        base_data = self.__get_base_data()
        imoveis = self.__get_imoveis_data()
        return dict(imoveis=imoveis, **base_data)

    def __get_base_data(self) -> dict:
        return {
            'EDITAL': self.wallet.modelo_edital,
            'DATA_PRIMEIRO_LEILAO': self.__format_date_leilao(self.properties[0].get('data_primeiro_leilao_data')),
            'DATA_SEGUNDO_LEILAO': self.__format_date_leilao(self.properties[0].get('data_segundo_leilao_data')),
            'VALOR_PRIMEIRO_LEILAO': self.properties[0].get('valor_primeiro_leilao_valor', 0),
            'VALOR_SEGUNDO_LEILAO': self.properties[0].get('valor_segundo_leilao_valor', 0),
            'NOME_CANAL_VENDA': self.cronograma.canal_venda_id,
            'NUMERO_LEILAO': self.wallet.numero_leilao,
            'PESSOA_ENCARREGADA': self.manager_responsible.nome if self.manager_responsible else "",
            'DATA': self.properties[0].get('data_limite').strftime("%d/%m/%Y") if self.properties[0].get('data_limite') else self.properties[0].get('data_primeiro_leilao_data').strftime("%d/%m/%Y") if self.properties[0].get('data_primeiro_leilao_data') else "",
            'HORA': self.properties[0].get('data_limite').strftime("%H:%M") if self.properties[0].get('data_limite') else self.properties[0].get('data_primeiro_leilao_data').strftime("%H:%M") if self.properties[0].get('data_primeiro_leilao_data') else "",
            'SITE': self.cronograma.site,
            'NOME_LEILOEIRO_OFICIAL': self.cronograma.responsavel_nome,
            'CPF_CNPJ': self.cronograma.responsavel_cpf,
            'UF_JUCESP': self.cronograma.uf_jucesp,
            'NUMERO_JUCESP': self.cronograma.numero_jucesp,
            'NOME_RESPONSAVEL': self.proponent[0].get('primeiro_nome') + self.proponent[0].get('ultimo_nome') if self.proponente else "",
            'ASSINANTE': self.proponent[0].get('primeiro_nome') + self.proponent[0].get('ultimo_nome') if self.proponente else self.cronograma.responsavel_nome,
            'CPF_RESPONSAVEL': self.proponent[0].get('cpf_cnpj') if self.proponente else "",
            'TELEFONE_RESPONSAVEL': self.proponent[0].get('telefone1') if self.proponente else self.cronograma.canal_responsavel_telefone,
            'EMAIL_RESPONSAVEL': self.proponent[0].get('email_address') if self.proponente else self.cronograma.responsavel_email,
            'RUA': f"{self.cronograma.endereco_rua}, {self.cronograma.endereco_numero}, {self.cronograma.endereco_bairro}",
            'COMPLEMENTO': '',
            'CIDADE': f"{self.cronograma.endereco_cidade}/{self.cronograma.endereco_estado}",
            'CEP': self.cronograma.endereco_cep,
            'PAGAMENTO_DINHEIRO': self.text_payments.get('condition_type_in_cash') if self.text_payments.get('condition_type_in_cash') else "",
            'PAGAMENTO_DINHEIRO_TEXTO': self.text_payments.get('cash_payment_text') if self.text_payments.get('cash_payment_text') else "",
            'PAGAMENTO_PARCELADO': self.text_payments.get('condition_type_installments') if self.text_payments.get('condition_type_installments') else "",
            'PAGAMENTO_PARCELADO_TEXTO': self.text_payments.get('parceled_payment_text') if self.text_payments.get('parceled_payment_text') else "",
            'CONDICOES_PAGAMENTO_DINHEIRO': self.text_payments.get('in_cash_payment_desc') if self.text_payments.get('in_cash_payment_desc') else "",
            'CONDICOES_PAGAMENTO_PARCELADO': self.text_payments.get('installments_payment_desc') if self.text_payments.get('installments_payment_desc') else "",
            'PAGAMENTO_FINANCIAMENTO_TEXTO':  self.text_payments.get('financing_payment_text') if self.text_payments.get('financing_payment_text') else "",
            'PAGAMENTO_FINANCIAMENTO':  self.text_payments.get('condition_type_financiado') if self.text_payments.get('condition_type_financiado') else "",
            'DIA_CORRENTE': datetime.now().strftime("%d"),
            'MES_CORRENTE': self.__month_in_full(datetime.now().strftime("%m")),
            'ANO_CORRENTE': datetime.now().strftime("%Y"),
            'TAXA_PAGIMOVEL':  round(self.wallet.tx_servico, 2) if self.wallet.tx_servico else 0,
            'TAXA_MINIMA': self.text_payments.get('taxa_maxima', 0) if self.text_payments.get('taxa_minima', 0) else 0,
            'TAXA_MAXIMA': self.text_payments.get('taxa_maxima', 0) if self.text_payments.get('taxa_maxima', 0) else 0
        }

    def __get_imoveis_data(self) -> dict:
        data = []
        for property in self.properties:
            considerations = get_property_considerations_full(property.get('imovel_id'), self.wallet.id)
            valor_proposto = property.get('valor_proposto', 0) if property.get('valor_proposto', 0) else 0
            pgi_amount = property.get('pgi_amount', 0) if property.get('pgi_amount', 0) else 0 
            data.append({
                "LOTE": property.get("lote") if property.get("lote") else "-",
                "ID_BANCO": property.get("id_no_banco") if property.get("id_no_banco") else "",
                "DESCRICAO_LEGAL": property.get("descricao_legal_description") if property.get("descricao_legal_description") else "",
                "CONSIDERACOES_IMPORTANTES": considerations if considerations else property.get("consideracoes_importantes"),
                "VALOR_VENDA": self.__return_sell_value(property),
                "VALOR_PRIMEIRO_LEILAO": number_format_money(property.get('valor_primeiro_leilao_valor') if property.get('valor_primeiro_leilao_valor', 0) else 0),
                "VALOR_SEGUNDO_LEILAO": number_format_money(property.get('valor_segundo_leilao_valor') if property.get('valor_segundo_leilao_valor', 0) else 0 ),
                "VALOR_PROPOSTO": self.__return_sell_value(property),
	            "VALOR_PGI": number_format_money(pgi_amount),
	            "VALOR_PROPOSTO": number_format_money(valor_proposto + pgi_amount)
            })
        return data

    @staticmethod
    def __format_date_leilao(date):
        if date:
            return f'{date.strftime("%d/%m/%Y")}, às {date.strftime("%H:%M")}'

        return ''

    def __return_sell_value(self, property):
        value = 0
        dict_value = get_property_valor_venda(property.get('imovel_id'), self.wallet.id)
        if dict_value:
            value = dict_value.get('valor_venda')

        if value:
            value = property.get('valor_proposto')

        return number_format_money(value)

    @staticmethod
    def __month_in_full(month: str):
        months = {
            "01": 'Janeiro',
            "02": 'Fevereiro',
            "03": 'Março',
            "04": 'Abril',
            "05": 'Maio',
            "06": 'Junho',
            "07": 'Julho',
            "08": 'Agosto',
            "09": 'Setembro',
            "10": 'Outubro',
            "11": 'Novembro',
            "12": 'Dezembro'
        }

        return months.get(month, '')
