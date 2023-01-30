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