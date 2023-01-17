from operator import and_
from api.common.database_common import DBSessionContext
from api.common.models import Manager, WalletManager, ManagerProperty, ManagerSalesCategory, Property


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

    def get_taxa_servico(self, property_id: str):
        with self.get_session_scope() as session:
            data = session.query(
                ManagerSalesCategory.taxa_servico_minima.label('cat_venda_tx_servico_min'),
                ManagerSalesCategory.taxa_servico_maxima.label('cat_venda_tx_servico_max'),
                Manager.taxa_servico_minima.label('gestor_tx_servico_min'),
            ).select_from(Manager) \
                .join(ManagerProperty, Manager.id == ManagerProperty.gestor_id) \
                .join(Property,  Property.id == ManagerProperty.imovel_id) \
                .join(ManagerSalesCategory, and_(ManagerSalesCategory.gestor_id == Manager.id,
                                                 ManagerSalesCategory.categoria_venda == Property.categoria_venda), isouter=True)\
                .filter(ManagerProperty.imovel_id == property_id).one()
        return data
