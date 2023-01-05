from utils.pagimovel_integrations.service import PagimovelIntegration
import locale
from celery import current_task
import os

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def get_property_valor_venda(property_id, wallet_id):
    if (os.environ.get("STAGE")).upper() == "LOCAL":
        return {"valor_avaliacao": 10000.32, "valor_venda": 30000.54} # MOCK

    return PagimovelIntegration().get_values(carteira_id=wallet_id, imovel_id=property_id)

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
    return locale.currency(number, grouping=True, symbol=None)

def update_task_progress(current: int, total: int):
    if current_task:
        current_task.update_state(state='PROGRESS', meta={
                        'current': current, 'total': total})