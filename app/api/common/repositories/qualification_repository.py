from api.common.database_common import DBSessionContext
from api.common.models import Qualification


class QualificationRepository(DBSessionContext):
    def fetch_qualifications_of_manager(self, manager: str):
        with self.get_session_scope() as session:
            qualification = session.query(Qualification.gestor_id,
                                          Qualification.conteudo) \
                .filter(Qualification.gestor_id == manager, Qualification.padrao_disputa_digital == True).all()
                
            return qualification
