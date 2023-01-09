from api.common.helpers import get_property_valor_venda


def set_property_valor(property_obj, wallet_id):
    property_values = get_property_valor_venda(property_id=property_obj.get("imovel_id"), wallet_id=wallet_id)
    valor_venda = property_values.get("valor_venda")

    property_obj["valor_proposto"] = valor_venda if valor_venda else property_obj["valor_proposto"]

    return property_obj