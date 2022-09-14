from utils.pagimovel_integrations.service import PagimovelIntegration


def get_property_valor_venda(property, wallet_id):
    return PagimovelIntegration().get_values(carteira_id=wallet_id, imovel_id=property.get("imovel_id"))

def transform_dict(list_of_tuples: list):
    return [dict(tuplas) for tuplas in list_of_tuples]

def number_format(number, decimal_places=2) -> str:
    if isinstance(number, str) and "," in number:
        number = number.replace(",", ".")

    number = round(float(number), decimal_places)

    if decimal_places == 0:
        number = int(number)

    return str(number).replace(".", ",")