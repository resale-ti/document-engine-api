from celery import Task
from core.celery import celery_app
from api.task_control.repositories import TaskControlRepository
from api.common.helpers import setting_application_manager_id


class TaskControlServices:
    def __init__(self):
        self.celery = celery_app
        self.task_control_repository = TaskControlRepository()

    def get_task_status(self, task_id):
        task = self.celery.AsyncResult(task_id)

        progression = None
        info = task.info

        if task.state not in ['FAILURE', 'PENDING', 'REVOKED']:
            current = task.info.get('current', 0)
            total = task.info.get('total', 1)
            progression = (int(current) / int(total)) * 100
            progression = progression - 1 if progression == 100 else progression

        if task.state == 'REVOKED':
            self.task_control_repository.update_task_state(task_id, 'REVOKED')

        return {
            'task_id': task_id,
            'state': task.state,
            'progression': float("{:.2f}".format(progression)) if progression is not None else None,
            'info': info
        }

    def get_last_task_by_owner_application_origin(self, requester_id, origin_application, manager_id=None):
        task = self.task_control_repository.get_last_task(requester_id, origin_application, manager_id)

        if task is not None:
            task = dict(task)
            result = self.celery.AsyncResult(task['task_id'])
            task['state'] = result.state
            task['result'] = result.result

        return task

    @staticmethod
    def send_task(task_params: dict):
        task_name = task_params.get('task_name')
        task_state = task_params.get('task_state')
        task_request = task_params.get('task_request')

        task = celery_app.send_task(task_name,
                                    kwargs={'task_request': dict(task_request)}, meta={'current': 0, 'total': 0})

        task_control_repository = TaskControlRepository()
        task_control_repository.save_task(task_id=task.id,
                                          task_name=task_name,
                                          task_state=task_state)

        return task
