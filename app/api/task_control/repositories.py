from datetime import datetime
from sqlalchemy import update

from api.common.database_common import DBSessionContext
from api.common.models import CeleryTask, Usuario


class TaskControlRepository(DBSessionContext):
    def get_last_task(self, item_origem_id, origin_application):
        filters = [CeleryTask.item_origem_id == item_origem_id,
                   CeleryTask.aplicacao_origem == origin_application]

        with self.get_session_scope() as session:
            return session.query(CeleryTask.id.label('task_id'))\
                .filter(*filters)\
                .order_by(CeleryTask.data_criacao.desc()).first()

    def save_task(self, **attrs):
        now = datetime.now()

        new_task_record = CeleryTask(
            id=attrs.get('task_id'),
            solicitante_id=attrs.get('requester_id'),
            aplicacao_origem=attrs.get('origin_application'),
            nome_tarefa=attrs.get('task_name'),
            situacao=attrs.get('task_state'),
            item_origem_id=attrs.get('item_origem_id'),
            gestor_id=attrs.get('manager_id'),
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

    def get_usuario(self, task_id: str) -> str:
        with self.get_session_scope() as session:
            result = session.query(Usuario.id, Usuario.first_name, Usuario.last_name).join(CeleryTask, CeleryTask.solicitante_id==Usuario.id).filter(CeleryTask.id == task_id).first()
            return {"id": result.id, "name": f"{result.first_name} {result.last_name}"}