from abc import ABC
import datetime
import os

from celery import current_task, Task
from core.celery import celery_app
from core.rollbar_celery import rollbar_celery

from api.contract.contract import Contract
from api.common.repositories.property_repository import PropertyRepository

from api.task_control.repositories import TaskControlRepository
from api.task_control.services import TaskControlServices
from api.task_control.progressbar import TaskProgress

from api.common.rollback.rollback_factory import RollbackFactory

from api.contract.regulamento_concorrencia.regulamento_conditions import ConditionsRegulamento

from utils.wuzu.auctions import Auctions


class CallbackTask(Task, ABC):
    def on_success(self, retval, task_id, args, kwargs):
        task_control_repository = TaskControlRepository()
        task_control_repository.update_task_state(task_id, 'SUCCESS')
        TaskControlServices.send_task_protection_state(False)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        task_control_repository = TaskControlRepository()
        task_control_repository.update_task_state(task_id, 'FAILURE')

        extra_data = {"task_id": task_id, "args": args, "kwargs": kwargs}
        rollbar_celery.report_exc_info(extra_data=extra_data)
        TaskControlServices.send_task_protection_state(False)

        print(f"kwargs: {kwargs}")

        contract_type = kwargs.get("task_request").get("contract_type")
        print(f"contract_type: {contract_type}")

        rb = RollbackFactory().get_instance(contract_type=contract_type, data=kwargs.get("task_request"))
        rb.handler()


@celery_app.task(
    name='regulamento_concorrencia_completo.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    data_inicio = task_request.get("data_inicio")
    print(f"data inicio : {data_inicio}")
    print(f"Data inicio tipo: {type(data_inicio)}")
    task_request["data_inicio"] = datetime.datetime.strptime(task_request.get("data_inicio"), "%Y-%m-%dT%H:%M:%S")
    task_request["data_fim"] = datetime.datetime.strptime(task_request.get("data_fim"), "%Y-%m-%dT%H:%M:%S")

    print(f"Iniciando Task p/ geração de Regulamento com payload: {task_request}")
    os.environ["REQUESTER_ID"] = task_request.get('requester_id')
    os.environ["DOCUMENT_ID_RC"] = ""

    cond_regulamento = ConditionsRegulamento(payload=task_request)
    cond_regulamento.execute_pre_conditions()

    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 0})

    carteira_id = task_request.get("id_obj")
    print(f"Iniciando geração de Auctions - Carteira: {carteira_id}")

    # Handled das auctions na Wuzu.
    Auctions().handle_auctions(task_request)

    # # Geração do Regulamento
    Contract.generate_contract(contract_type="regulamento_concorrencia", data=task_request)

    # # Geração do Certificado Venda
    properties = PropertyRepository().get_properties_wallet_with_schedule(wallet_id=carteira_id)

    for idx, prop in enumerate(properties):
        data = {"id_obj": carteira_id, "property_id": prop.imovel_id}
        print(f"Gerando CV p/ idx: {idx} - Imovel: {prop.imovel_id}")
        Contract.generate_contract(contract_type="certificado_venda", data=data)

        if idx % 5 == 0:
            print(f"Updated Task Progress p/ o idx {idx}")
            TaskProgress.update_task_progress()

    os.environ["DOCUMENT_ID_RC"] = ""


@celery_app.task(
    name='regulamento_concorrencia.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    data_inicio = task_request.get("data_inicio")
    print(f"data inicio : {data_inicio}")
    print(f"Data inicio tipo: {type(data_inicio)}")
    
    task_request["data_inicio"] = datetime.datetime.strptime(task_request.get("data_inicio"), "%Y-%m-%dT%H:%M:%S")
    task_request["data_fim"] = datetime.datetime.strptime(task_request.get("data_fim"), "%Y-%m-%dT%H:%M:%S")

    print(f"Iniciando Task p/ geração de Regulamento com payload: {task_request}")
    os.environ["REQUESTER_ID"] = task_request.get('requester_id')
    os.environ["DOCUMENT_ID_RC"] = ""

    cond_regulamento = ConditionsRegulamento(payload=task_request)
    cond_regulamento.execute_pre_conditions()

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
    
@celery_app.task(
    name='edital.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 6})

    contract_type = "edital"

    Contract.generate_contract(contract_type=contract_type, data=task_request)
