from api.common.database_common import DBSessionContext
from api.common.models import Wallet, Property, Manager, Schedule, DisputaWuzu, WalletProperty, WalletSchedule, WalletManager
from sqlalchemy import func, and_, or_


class PropertyRepository(DBSessionContext):
    def get_properties_wallet(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.lote,
                Property.id_no_banco,
                Property.descricao_legal_description,
                Property.consideracoes_importantes,
                Property.valor_proposto,
                Property.valor_minimo,
                (Property.valor_proposto * (Wallet.tx_servico / 100)).label('pgi_amount'),
                Property.imovel_origem,
                Property.data_limite,
                Property.data_primeiro_leilao_data,
                Property.data_segundo_leilao_data,
                Property.valor_primeiro_leilao_valor,
                Property.valor_segundo_leilao_valor,
                Property.id.label('imovel_id'),
                Property.nome,
                Property.idr_imovel,
                Manager.id.label('manager_id'),
                Manager.nome.label('manager_name'),
                Manager.url_whitelabel.label('gestor_url'),
                Schedule.id.label('schedule_id'),
                DisputaWuzu.status,
                DisputaWuzu.wuzu_disputa_id.label('auction_id'),
                DisputaWuzu.wuzu_status,
                DisputaWuzu.data_inicio_disputa) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                .join(Schedule, WalletSchedule.cronograma_id == Schedule.id) \
                .join(DisputaWuzu, and_(DisputaWuzu.imovel_id == Property.id,
                                        Schedule.id == DisputaWuzu.cronograma_id,
                                        DisputaWuzu.wuzu_status != 'canceled'), isouter=True) \
                .filter(Wallet.id == wallet_id,
                        and_(Schedule.data_inicio <= func.current_date(), Schedule.data_final >= func.current_date()),
                        or_(DisputaWuzu.wuzu_status == None, DisputaWuzu.wuzu_status.not_in(['canceled', 'closed']))) \
                .group_by(Property.id) \
                .order_by(Property.lote).all()

            return properties

    def get_properties_wallet_to_wuzu(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.id.label('imovel_id'),
                Property.data_limite,
                Schedule.id.label('schedule_id'),
                DisputaWuzu.wuzu_disputa_id) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                .join(Schedule, WalletSchedule.cronograma_id == Schedule.id) \
                .join(DisputaWuzu, and_(DisputaWuzu.imovel_id == Property.id,
                                        Schedule.id == DisputaWuzu.cronograma_id,
                                        DisputaWuzu.wuzu_status != 'canceled'), isouter=True) \
                .filter(Wallet.id == wallet_id).all()

            return properties