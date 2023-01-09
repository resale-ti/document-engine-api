from celery import current_task
from core.celery import celery_app


class TaskProgress:

    @staticmethod
    def get_current_task(task_id):
        my_task = celery_app.AsyncResult(task_id)
        return {"current": my_task.info.get("current"), "total": my_task.info.get("total")}

    @staticmethod
    def update_task_progress(total=None):
        if current_task:
            current = 0
            total = total

            if total is None:
                my_task = TaskProgress.get_current_task(current_task.request.id)
                current = int(my_task.get("current")) + 1
                total = int(my_task.get("total"))

            current_task.update_state(state='PROGRESS', meta={
                'current': current, 'total': total})
