from fastapi import APIRouter, status, Response
from api.contract.schemas import ContractBaseSchema, RegulamentoSchema
from api.task_control.services import TaskControlServices

from utils.rollbar_handler import response_rollbar_handler

router = APIRouter()


@router.post("/regulamento-concorrencia-completo", status_code=status.HTTP_200_OK)
async def generate_celery(payload: RegulamentoSchema, response: Response) -> dict:
    try:
        task = TaskControlServices.send_task({
            'task_name': f'regulamento_concorrencia_completo.generate_document',
            'task_state': 'PENDING',
            'task_request': payload
        })

        return {'task': task.task_id, 'message': 'Solicitação recebida com sucesso!'}

    except Exception as err:
        return response_rollbar_handler(err, response)


@router.post("/regulamento-concorrencia", status_code=status.HTTP_200_OK)
async def generate_celery(payload: RegulamentoSchema, response: Response) -> dict:
    try:
        task = TaskControlServices.send_task({
            'task_name': f'regulamento-concorrencia.generate_document',
            'task_state': 'PENDING',
            'task_request': payload
        })

        return {'task': task.task_id, 'message': 'Solicitação recebida com sucesso!'}

    except Exception as err:
        return response_rollbar_handler(err, response)


@router.post("/certificado-venda", status_code=status.HTTP_200_OK)
async def generate_celery(payload: ContractBaseSchema, response: Response) -> dict:
    try:
        task = TaskControlServices.send_task({
            'task_name': f'certificado_venda.generate_document',
            'task_state': 'PENDING',
            'task_request': payload
        })

        return {'task': task.task_id, 'message': 'Solicitação recebida com sucesso!'}

    except Exception as err:
        return response_rollbar_handler(err, response)