from utils.pagimovel_integrations.service import PagimovelIntegration
from celery import current_task
import os

def get_property_valor_venda(property_id, wallet_id):
    if (os.environ.get("STAGE")).upper() == "LOCAL":
        return {"valor_avaliacao": 10000.32, "valor_venda": 30000.54} # MOCK

    return PagimovelIntegration().get_values(carteira_id=wallet_id, imovel_id=property_id)

def get_property_considerations_full(property_id, wallet_id):
    return PagimovelIntegration().get_considerations(carteira_id=wallet_id, imovel_id=property_id)

def transform_dict(list_of_tuples: list):
    return [dict(tuplas) for tuplas in list_of_tuples]

def number_format(number, decimal_places=2) -> str:
    if isinstance(number, str) and "," in number:
        number = number.replace(",", ".")

    number = round(float(number), decimal_places)

    if decimal_places == 0:
        number = int(number)

    return str(number).replace(".", ",")

def parse_to_money(number) -> str:
    """
    Formata um número para o formato monetário brasileiro (sem símbolo R$).
    Ex: 1234.56 -> '1.234,56'
    """
    if number is None:
        number = 0
    
    # Converte para float e formata com 2 casas decimais
    value = float(number)
    
    # Formata com 2 casas decimais
    formatted = f"{value:,.2f}"
    
    # Substitui vírgula por ponto (milhar) e ponto por vírgula (decimal)
    # formato americano: 1,234.56 -> formato brasileiro: 1.234,56
    formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
    
    return formatted

def update_task_progress(current: int, total: int):
    if current_task:
        current_task.update_state(state='PROGRESS', meta={
                        'current': current, 'total': total})