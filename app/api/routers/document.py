from fastapi import APIRouter, status, Response
from api.contract.schemas import ContractSchema
from api.task_control.services import TaskControlServices
from api.contract.contract_enum import EnumContractType

from utils.rollbar_handler import response_rollbar_handler

router = APIRouter()


@router.post("/contract-generate", status_code=status.HTTP_200_OK)
async def generate_celery(payload: ContractSchema, response: Response) -> dict:
    try:
        if payload.contract_type not in [ct.value for ct in EnumContractType]:
            raise Exception("Insert a valid type of ContractType.")

        task = TaskControlServices.send_task({
            'task_name': 'contract.generate_document',
            'task_state': 'PENDING',
            'task_request': payload
        })
        return {'task': payload, 'message': 'Solicitação recebida com sucesso!'}

    except Exception as err:
        return response_rollbar_handler(err, response)
