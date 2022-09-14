from api.common.helpers import get_property_valor_venda


def set_property_valor(property, wallet_id):
    property_values = get_property_valor_venda(property=property, wallet_id=wallet_id)
    valor_venda = property_values.get("valor_venda")

    property["valor_proposto"] = valor_venda if valor_venda else property["valor_proposto"]

    return property