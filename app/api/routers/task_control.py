from fastapi import APIRouter, Depends, Response

from api.task_control.services import TaskControlServices
from utils.rollbar_handler import response_rollbar_handler

router = APIRouter()


@router.get("/status/{task_id}")
def get_status(task_id, response: Response):
    try:
        task_control_services = TaskControlServices()

        return task_control_services.get_task_status(task_id)

    except Exception as err:
        return response_rollbar_handler(err, response)


@router.get('/last/{requester_id}/{origin_application}')
def get_last_task(requester_id, origin_application, response: Response):
    try:
        task_control_services = TaskControlServices()

        return task_control_services.get_last_task_by_owner_application_origin(requester_id=requester_id,
                                                                           origin_application=origin_application)

    except Exception as err:
        return response_rollbar_handler(err, response)

