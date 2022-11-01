from api.common.database_common import DBSessionContext
from api.common.models import Manager, WalletManager


class ManagerRepository(DBSessionContext):
    def get_manager_by_wallet_id(self, wallet_id):
        with self.get_session_scope() as session:
            manager = session.query(
                Manager.id,
                Manager.nome,
                Manager.slug,
                Manager.url_whitelabel
            ).join(WalletManager, Manager.id == WalletManager.gestor_id) \
            .filter(WalletManager.carteira_id == wallet_id).one()

            return manager
