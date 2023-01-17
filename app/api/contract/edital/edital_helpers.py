from api.common.helpers import get_property_valor_venda


def set_property_valor(property, wallet_id):
    return property

def number_format(number):
    if number:
        return (str(round(number, 2))).replace(',', '').replace('.', ',')
    return '0,00'

def number_format_money(number):
    if number:
        return f'R$ {number_format(number)}'
    return 'R$ 0,00'
    


def normalize_payment_method(field):
    if 'sim':
        return 'Sim'
    elif 'nao':
        return 'Não'
    elif 'price':
        return 'PRICE'
    elif 'sac':
        return 'SAC'
    elif 'igpm':
        return 'IGP-M'
    elif 'ipca':
        return 'IPCA'
    elif 'tr':
        return 'TR'
    elif 'outro':
        return 'Outro'
    elif 'sacre':
        return 'SACRE'
    elif 'incc':
        return 'INCC'
    else:
        return ''