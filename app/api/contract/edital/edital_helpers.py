from api.common.repositories.payment_repository import PaymentRepository

def number_format(number):
    if number:
        return (str(round(number, 2))).replace(',', '').replace('.', ',')
    return '0,00'

def number_format_money(number):
    if number:
        return f'R$ {number_format(number)}'
    return 'R$ 0,00'

def normalize_payment_method(field: str):
    payment_methods = {
        'sim': 'Sim',
        'nao': 'Não',
        'price': 'PRICE',
        'sac': 'SAC',
        'igpm': 'IGP-M',
        'ipca': 'IPCA',
        'tr':'TR',
        'outro':'Outro',
        'sacre':'SACRE',
        'incc':'INCC'
    }

    return payment_methods.get(field, '')

def mount_text_payments(payment_methods):
    dict_ = {}
    for p in payment_methods:
        if p.get('tipo_condicao') == 'vista':
            dict_['condition_type_in_cash'] = 'X'

            if p.get('porcentagem_sinal', 0) > 0:
                dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + number_format(p.get('porcentagem_sinal', '0')) + \
                    r'% de entrada, '

            if p.get('porcentagem_ccv', 0) > 0:
                dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + number_format(p.get('porcentagem_ccv', '0')) + \
                    r'% do pagamento na emissão do CCV (Contrato de Compra e Venda)'

            if p.get('porcentagem_escritura', 0) > 0:
                dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + ', ' + number_format(p.get('porcentagem_escritura', '0')) + \
                    r'% na escritura'

            if p.get('a_vista_desconto', 0) > 0:
                dict_['in_cash_payment_desc'] = dict_.get('in_cash_payment_desc', '') + ', c/ ' + number_format(p.get('a_vista_desconto', '0')) + \
                    r'% de desconto sobre o valor do lance vencedor'

        if p.get('tipo_condicao') == 'financiado':
            dict_['condition_type_financiado'] = 'X'

            if p.get('porcentagem_entrada_financiamento', 0) > 0:
                dict_['financing_payment_text'] = number_format(
                    p.get('porcentagem_entrada_financiamento')) + r'% de entrada'

        if p.get('tipo_condicao') == 'parcelado':
            dict_['cash_payment_text'] = f" {p.get('a_vista_complemento_texto')}" if p.get(
                'a_vista_complemento_texto') else ''
            dict_['parceled_payment_text'] = f"  {p.get('parcelado_complemento_texto')}" if p.get(
                'parcelado_complemento_texto') else ''
            dict_['financing_payment_text'] = f"  {p.get('financiamento_complemento_texto')}" if p.get(
                'financiamento_complemento_texto') else ''

            dict_['condition_type_installments'] = 'X'
            payment_installments = PaymentRepository().get_payment_installments(
                payment_condition_id=p.get('id'))

            if payment_installments[0].get('qtd_fixa'):
                sorted(payment_installments, key=lambda x: x.get(
                    'qtd_fixa'), reverse=True)
            else:
                sorted(payment_installments, key=lambda x: x.get(
                    'qtd_maxima'), reverse=True)

            payment_installments = payment_installments[0]

            dict_['entry_percent'] = payment_installments.get(
                'porcentagem_entrada', '0')

            dict_['installments_payment_desc'] = number_format(
                dict_.get('entry_percent')) + r'% de entrada e '

            dict_['interest_period'] = payment_installments.get(
                'periodo_juros') if payment_installments.get('periodo_juros') else 'a.m.'
            dict_['interest_rate'] = ((payment_installments.get(
                'tx_juros') if payment_installments.get('tx_juros') else 0) * 100) / 100

            dict_['correction_period'] = payment_installments.get(
                'periodo_correcao') if payment_installments.get('periodo_correcao') else 'a.m.'
            dict_['correction_rate'] = ((payment_installments.get(
                'tx_correcao') if payment_installments.get('tx_correcao') else 0) * 100) / 100

            dict_['indexador'] = normalize_payment_method(
                payment_installments.get('indexador'))

            if payment_installments.get('qtd_fixa') > 0:
                dict_[
                    'installments_payment_desc'] = f"{dict_.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_fixa')} "
                f"parcelas com juros de {number_format(dict_.get('interest_rate', ''))}% {dict_.get('interest_period', '')}"
            else:
                dict_[
                    'installments_payment_desc'] = f"{dict_.get('installments_payment_desc', '')}saldo em até {payment_installments.get('qtd_maxima')} "
                f"parcelas com juros de {number_format(dict_.get('interest_rate', ''))}% {dict_.get('interest_period', '')}"

            if dict_.get('correction_rate'):
                dict_['installments_payment_desc'] = dict_.get(
                    'installments_payment_desc', '')
                f" + correção de {number_format(dict_.get('correction_rate', ''))}% {dict_.get('correction_period', '')}"

            if dict_.get('indexador'):
                dict_['installments_payment_desc'] = dict_.get(
                    'installments_payment_desc', '') + f" + {dict_.get('indexador', '')}"

    return dict_
