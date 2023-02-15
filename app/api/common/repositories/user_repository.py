from api.common.database_common import DBSessionContext
from api.common.models import Usuario


class UserRepository(DBSessionContext):

    def get_user_detail(self, user_id):
        with self.get_session_scope() as session:
            user = session.query(
                Usuario.username,
                Usuario.email) \
                .select_from(Usuario) \
                .filter(Usuario.id == user_id) \
                .one_or_none()

            return user
