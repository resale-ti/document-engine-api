from decimal import Decimal
import datetime
from utils.dotdict import dotdict


WALLET_MOCK = dotdict({
    "modelo_regulamento": "MLP_002",
    "disputa_id": "MPR202201234",
    "tx_servico": Decimal('1.50'),
    "tx_comissao": Decimal('5.00')
})

PAYMENT_METHODS_MOCK = [
    {'id': 1730, 'tipo_condicao': 'parcelado', 'vendedor_id': 'b9be8d34-2a93-562e-b...bab630e786',
     'status': 'ativo', 'porcentagem_sinal': None, 'porcentagem_ccv': None, 'porcentagem_escritura': None,
     'a_vista_desconto': None, 'installments_db': [{'qtd_fixa': 0, 'qtd_maxima': 3, 'porcentagem_entrada': 30}]},
    {'id': 1731, 'tipo_condicao': 'vista', 'vendedor_id': 'b9be8d34-2a93-562e-b...bab630e786', 'status': 'ativo',
     'porcentagem_sinal': 0, 'porcentagem_ccv': 100, 'porcentagem_escritura': 0, 'a_vista_desconto': Decimal('0.000000')}]


PROPERTY_MOCK = [
    {
        'data_limite': datetime.datetime(2022, 10, 6, 13, 0),
        'data_primeiro_leilao_data': datetime.datetime(2022, 9, 26, 15, 0),
        'data_segundo_leilao_data': datetime.datetime(2022, 9, 28, 15, 0),
        'valor_primeiro_leilao_valor': Decimal('138000.00000000'),
        'valor_segundo_leilao_valor': Decimal('220061.58000000'),
        'imovel_id': '54e62b3f-d4e0-4177-8178-bcdbd268926e',
        'nome': 'Apartamento, Residencial, Campos Elíseos, 1 dormitório(s)',
        'idr_imovel': 'IDR175048',
        'manager_id': 'b9be8d34-2a93-562e-b5f1-5ebab630e786',
        'manager_name': 'Emgea',
        'gestor_url': 'https://emgeaimoveis.com.br/',
        'schedule_id': '39b5c160-f69e-4518-9f66-0505d63f784d',
        'status': 'approve',
        'auction_id': '2725',
        'wuzu_status': 'opened',
        'data_inicio_disputa': datetime.datetime(2022, 10, 4, 13, 0)
    }]

QUALIFICACAO_MOCK = [dotdict({"conteudo": "Disputa Digital"})]

REGULAMENTO_DATES_MOCK = {
    'data_inicio': datetime.datetime(2022, 10, 25, 12, 0),
    'data_fim': datetime.datetime.today() + datetime.timedelta(hours=1)}
