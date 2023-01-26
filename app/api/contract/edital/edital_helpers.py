def number_format(number):
    if number:
        return (str(round(number, 2))).replace(',', '').replace('.', ',')
    return '0,00'

def number_format_money(number):
    if number:
        return f'R$ {number_format(number)}'
    return 'R$ 0,00'

def normalize_payment_method(field):
    if field =='sim':
        return 'Sim'
    elif field == 'nao':
        return 'Não'
    elif field == 'price':
        return 'PRICE'
    elif field == 'sac':
        return 'SAC'
    elif field == 'igpm':
        return 'IGP-M'
    elif field == 'ipca':
        return 'IPCA'
    elif field == 'tr':
        return 'TR'
    elif field == 'outro':
        return 'Outro'
    elif field == 'sacre':
        return 'SACRE'
    elif field == 'incc':
        return 'INCC'
    else:
        return ''