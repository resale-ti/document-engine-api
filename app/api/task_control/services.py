from celery import Task
from core.celery import celery_app
from api.task_control.repositories import TaskControlRepository
from datetime import timedelta


class TaskControlServices:
    def __init__(self):
        self.celery = celery_app
        self.task_control_repository = TaskControlRepository()

    def get_task_status(self, task_id):
        task = self.celery.AsyncResult(task_id)

        progression = None
        info = task.info

        if task.state not in ['FAILURE', 'PENDING', 'REVOKED', 'SUCCESS']:
            current = int(task.info.get('current', 0))
            total = int(task.info.get('total', 1))
            progression = (current/total) * 100 if total > 0 else 0
            progression = progression - 1 if progression == 100 else progression

        if task.state == 'REVOKED':
            self.task_control_repository.update_task_state(task_id, 'REVOKED')

        date = ""
        date_done = task.date_done

        if date_done is not None:
                date = (date_done - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M')

        return {
            'task_id': task_id,
            'state': task.state,
            'date': date,
            'progression': float("{:.2f}".format(progression)) if progression is not None else None,
            'info': info
        }

    def get_last_task_by_item_origem_application_origin(self, item_origem_id, origin_application):
        task = self.task_control_repository.get_last_task(item_origem_id, origin_application)
        date_done = None

        if task is not None:
            user = self.task_control_repository.get_usuario(task['task_id'])

            task = dict(task)
            result = self.celery.AsyncResult(task['task_id'])
            task['user_id'] = user.get("id")
            task['user'] = user.get("name")
            task['state'] = result.state
            task['result'] = result.result

            date_done = result.date_done

        if date_done is not None:
            task['date'] = (date_done - timedelta(hours=3)).strftime('%d/%m/%Y %H:%M')

        return task

    def revoke_task(self, task_id):
        task = self.celery.AsyncResult(task_id)
        if task.state not in ['FAILURE', 'SUCCESS']:
            self.celery.control.revoke(task_id, terminate=True)
            self.task_control_repository.update_task_state(task_id, 'REVOKED')
            self.celery.backend.store_result(task_id=task_id, state='REVOKED', result={})

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
                                          task_state=task_state,
                                          requester_id=task_request.requester_id,
                                          origin_application=task_request.origin_application,
                                          item_origem_id=task_request.id_obj,
                                          manager_id=task_request.manager_id,
                                          payload=task_request)

        return task
