from datetime import datetime
from sqlalchemy import update

from api.common.database_common import DBSessionContext
from api.common.models import CeleryTask


class TaskControlRepository(DBSessionContext):
    def get_last_task(self, requester_id, origin_application, manager_id=None):
        filters = [CeleryTask.solicitante_id == requester_id,
                   CeleryTask.aplicacao_origem == origin_application]
        if manager_id is not None:
            filters.append(CeleryTask.gestor_id == manager_id)

        with self.get_session_scope() as session:
            return session.query(CeleryTask.id.label('task_id'))\
                .filter(*filters)\
                .order_by(CeleryTask.data_criacao.desc()).first()

    def save_task(self, **attrs):
        now = datetime.now()

        new_task_record = CeleryTask(
            id=attrs.get('task_id'),
            nome_tarefa=attrs.get('task_name'),
            situacao=attrs.get('task_state'),
            data_criacao=now,
            data_modificacao=now
        )

        with self.get_session_scope() as session:
            session.add(new_task_record)

    def update_task_state(self, task_id, state):
        with self.get_session_scope() as session:
            session.execute(
                update(CeleryTask)
                .where(CeleryTask.id == task_id, CeleryTask.situacao != state)
                .values(situacao=state)
            )
