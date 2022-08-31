from app.utils.pagimovel_integrations.service import PagimovelIntegration


def get_property_valor_venda(property, wallet_id):
    return PagimovelIntegration().get_values(carteira_id=wallet_id, imovel_id=property.get("imovel_id"))

def transform_dict(list_of_tuples: list):
    return [dict(tuplas) for tuplas in list_of_tuples]