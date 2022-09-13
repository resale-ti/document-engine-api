from fastapi import APIRouter, status, Response
from api.contract.contract import Contract
from api.task_control.services import TaskControlServices

from utils.rollbar_handler import response_rollbar_handler

router = APIRouter()

@router.get('/fastapi/{contract_type}/{id}')
async def generate_fastapi(contract_type: str, id: str):
    result = Contract.generate_contract(contract_type=contract_type, data={"id": id})
    return {"status": 200}


@router.get("/{contract_type}/{id_obj}")
async def generate_celery(contract_type: str, id_obj: str) -> dict:
    task = TaskControlServices.send_task({
        'task_name': f'{contract_type}.generate_document',
        'task_state': 'PENDING',
        'task_request': {"contract_type": contract_type, "id": id_obj}
    })

    return {'task': task.task_id, 'message': 'Solicitação recebida com sucesso!'}
