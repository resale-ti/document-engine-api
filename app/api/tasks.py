from abc import ABC
import datetime

from celery import current_task, Task
from core.celery import celery_app
from core.rollbar_celery import rollbar_celery

from api.contract.contract import Contract
from api.common.repositories.property_repository import PropertyRepository

from api.task_control.repositories import TaskControlRepository
from api.task_control.progressbar import TaskProgress

from utils.wuzu.auctions import Auctions


class CallbackTask(Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        task_control_repository = TaskControlRepository()
        task_control_repository.update_task_state(task_id, 'SUCCESS')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_control_repository = TaskControlRepository()
        task_control_repository.update_task_state(task_id, 'FAILURE')
        extra_data = {"task_id": task_id, "args": args, "kwargs": kwargs}
        rollbar_celery.report_exc_info(extra_data=extra_data)


@celery_app.task(
    name='regulamento_concorrencia_completo.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 0})
    contract_type = "regulamento_concorrencia"
    task_request["data_inicio"] = datetime.datetime.strptime(task_request["data_inicio"], "%Y-%m-%dT%H:%M:%S")
    carteira_id = task_request.get("id_obj")

    # Handled das auctions na Wuzu.
    Auctions().handle_auctions(task_request)

    # # Geração do Regulamento
    Contract.generate_contract(contract_type=contract_type, data=task_request)

    # # Geração do Certificado Venda
    properties = PropertyRepository().get_properties_wallet_with_disputa(wallet_id=carteira_id)

    for idx, prop in enumerate(properties):
        data = {"id_obj": carteira_id, "property_id": prop.imovel_id}
        print(f"Gerando CV p/ idx: {idx} - Imovel: {prop.imovel_id}")
        Contract.generate_contract(contract_type="certificado_venda", data=data)

        if idx % 5 == 0:
            print(f"Updated Task Progress p/ o idx {idx}")
            TaskProgress.update_task_progress()


@celery_app.task(
    name='regulamento_concorrencia.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 1})

    contract_type = "regulamento_concorrencia"

    Contract.generate_contract(contract_type=contract_type, data=task_request)


@celery_app.task(
    name='certificado_venda.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 1})

    contract_type = "certificado_venda"

    Contract.generate_contract(contract_type=contract_type, data=task_request)

    # regulamento_cv vai ser chamado aqui passando a carteira e ele se vira pra lá
