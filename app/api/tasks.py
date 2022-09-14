from abc import ABC
from celery import current_task, Task

from core.celery import celery_app

from api.contract.contract import Contract
from api.task_control.repositories import TaskControlRepository
from core.rollbar_celery import rollbar_celery


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
    name='contract.generate_document',
    base=CallbackTask,
)
def generate_document(task_request: dict) -> str:
    current_task.update_state(state='STARTED', meta={'current': 0, 'total': 1})

    contract_type = task_request.get("contract_type")

    # No futuro no data pode ser o task_request completo. - VER A NECESSIDADE.
    Contract.generate_contract(contract_type=contract_type, data={"id_obj": task_request.get("id_obj")})

