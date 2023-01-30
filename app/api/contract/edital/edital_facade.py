from api.common.helpers import get_property_valor_venda, get_property_considerations_full
from api.contract.edital.edital_helpers import number_format_money
from api.contract.contract_builder_interface import ContractFacadeInterface
from datetime import datetime


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

        return dict(imoveis=imoveis, **base_data)

    def __get_base_data(self) -> dict:
        return {
            'edital': self.wallet.modelo_edital,
            'primeiro_leilao_data_c': self.__format_date_leilao(self.properties[0].get('data_primeiro_leilao_data')),
            'segundo_leilao_data_c': self.__format_date_leilao(self.properties[0].get('data_segundo_leilao_data')),
            'primeiro_leilao_valor_c': self.properties[0].get('valor_primeiro_leilao_valor', 0),
            'segundo_leilao_valor_c': self.properties[0].get('valor_segundo_leilao_valor', 0),
            'canal_venda_name': self.cronograma.canal_venda_id,
            'nome_leiloeiro_oficial_c': self.cronograma.canal_venda_id,
            'numero_leilao_c': self.wallet.numero_leilao,
            'person_in_charge': self.manager_responsible.nome if self.manager_responsible else "",
            'date': self.properties[0].get('data_limite').strftime("%d/%m/%Y") if self.properties[0].get('data_limite') else self.properties[0].get('data_primeiro_leilao_data').strftime("%d/%m/%Y"),
            'time': self.properties[0].get('data_limite').strftime("%H:%M") if self.properties[0].get('data_limite') else self.properties[0].get('data_primeiro_leilao_data').strftime("%H:%M"),
            'site_c': self.cronograma.site,
            'nome_leiloeiro_oficial_c': self.cronograma.responsavel_nome,
            'cpf_cnpj_c': self.cronograma.responsavel_cpf,
            'uf_jucesp_c': self.cronograma.uf_jucesp,
            'numero_jucesp_c': self.cronograma.numero_jucesp,
            'responsavel_nome_c': self.proponent[0].get('primeiro_nome') + self.proponent[0].get('ultimo_nome') if self.proponente else "",
            'signer': self.proponent[0].get('primeiro_nome') + self.proponent[0].get('ultimo_nome') if self.proponente else self.cronograma.responsavel_nome,
            'responsavel_cpf_c': self.proponent[0].get('cpf_cnpj') if self.proponente else "",
            'responsavel_telefone_c': self.proponent[0].get('telefone1') if self.proponente else self.cronograma.canal_responsavel_telefone,
            'responsavel_email_c': self.proponent[0].get('email_address') if self.proponente else self.cronograma.responsavel_email,
            'street_adress_c': f"{self.cronograma.endereco_rua}, {self.cronograma.endereco_numero}, {self.cronograma.endereco_bairro}",
            'complement': '',
            'city_adress_c': f"{self.cronograma.endereco_cidade}/{self.cronograma.endereco_estado}",
            'postal_code_adress_c': self.cronograma.endereco_cep,
            'cash_payment': self.aux.get('condition_type_in_cash'),
            'cash_payment_text': self.aux.get('cash_payment_text'),
            'installments_payment': self.aux.get('condition_type_installments'),
            'parceled_payment_text': self.aux.get('parceled_payment_text'),
            'payment_conditions_cash': self.aux.get('in_cash_payment_desc'),
            'payment_conditions_installments': self.aux.get('installments_payment_desc'),
            'financing_payment_text': self.aux.get('financing_payment_text'),
            'condition_type_financiado': self.aux.get('condition_type_financiado'),
            'current_day': datetime.now().strftime("%d"),
            'current_month': self.__month_in_full(datetime.now().strftime("%m")),
            'current_year': datetime.now().strftime("%Y"),
            'taxa_pagimovel':  round(self.wallet.tx_servico, 2) if self.wallet.tx_servico else 0,
            'taxa_minima': self.aux.get('taxa_minima', 0),
            'taxa_maxima': self.aux.get('taxa_maxima', 0)
        }

    def __get_imoveis_data(self) -> dict:
        data = []
        for property in self.properties:
            considerations = get_property_considerations_full(property.get('imovel_id'), self.wallet.id)
            data.append({
                "lote_c": property.get("lote") if property.get("lote") else "-",
                "id_banco_c": property.get("id_no_banco") if property.get("id_no_banco") else "",
                "legal_description_c": property.get("descricao_legal_description") if property.get("descricao_legal_description") else "",
                "consideracoes_importantes_c": considerations if considerations else property.get("consideracoes_importantes"),
                "valor_venda": self.__return_sell_value(property),
                "primeiro_leilao_valor_c": number_format_money(property.get('valor_primeiro_leilao_valor', 0)),
                "segundo_leilao_valor_c": number_format_money(property.get('valor_segundo_leilao_valor', 0)),
                "valor_proposto_c": self.__return_sell_value(property),
	            "pgi_amount": number_format_money(property.get('pgi_amount', 0)),
	            "valor_minimo_c": number_format_money(property.get('valor_proposto', 0) + property.get('pgi_amount', 0))
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
