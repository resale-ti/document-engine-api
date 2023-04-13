from api.common.database_common import DBSessionContext
from api.common.models import Wallet, Property, Manager, Schedule, DisputaWuzu, WalletProperty, WalletSchedule, \
    WalletManager, City, Address, PropertyAddress, Seller, SellerProperty
from api.common.repositories.history_repository import HistoryRepository
from sqlalchemy import func, and_, or_, update
from api.common.helpers import transform_dict


class PropertyRepository(DBSessionContext):

    def get_property_detail_by_wallet(self, imovel_id, wallet_id):
        with self.get_session_scope() as session:
            property_obj = session.query(
                Property.id.label('imovel_id'),
                Property.data_limite,
                Property.lote) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .filter(Wallet.id == wallet_id, Property.id == imovel_id).one()

            return property_obj

    def get_properties_wallet_with_disputa(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.lote,
                Property.id_no_banco,
                Property.descricao_legal_description,
                Property.consideracoes_importantes,
                Property.valor_proposto,
                Property.valor_minimo,
                (Property.valor_proposto *
                 (Wallet.tx_servico / 100)).label('pgi_amount'),
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
                        and_(Schedule.data_inicio <= func.current_date(),
                             Schedule.data_final >= func.current_date()),
                        or_(DisputaWuzu.wuzu_status == None, DisputaWuzu.wuzu_status.not_in(['canceled', 'closed']))) \
                .group_by(Property.id) \
                .order_by(Property.lote).all()

            return properties
        
    def get_properties_wallet_with_schedule(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.lote,
                Property.id_no_banco,
                Property.descricao_legal_description,
                Property.consideracoes_importantes,
                Property.valor_proposto,
                Property.valor_minimo,
                (Property.valor_proposto *
                 (Wallet.tx_servico / 100)).label('pgi_amount'),
                Property.imovel_origem,
                Property.data_limite,
                Property.data_primeiro_leilao_data,
                Property.data_segundo_leilao_data,
                Property.valor_primeiro_leilao_valor,
                Property.valor_segundo_leilao_valor,
                Property.id.label('imovel_id'),
                Property.nome,
                Property.idr_imovel,
                Wallet.codigo,
                Manager.id.label('manager_id'),
                Manager.nome.label('manager_name'),
                Manager.url_whitelabel.label('gestor_url'),
                Schedule.id.label('schedule_id')) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                .join(Schedule, WalletSchedule.cronograma_id == Schedule.id) \
                .filter(Wallet.id == wallet_id,
                        and_(Schedule.data_inicio <= func.current_date(),
                             Schedule.data_final >= func.current_date())) \
                .group_by(Property.id) \
                .order_by(Property.lote).all()

            return properties

    def get_properties_wallet_to_wuzu(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.id.label('imovel_id'),
                Property.data_limite,
                Schedule.id.label('schedule_id'),
                Property.idr_imovel.label('idr'),
                Wallet.codigo,
                Wallet.tipo_cofre,
                DisputaWuzu.wuzu_disputa_id,
                DisputaWuzu.data_inicio_disputa,
                DisputaWuzu.data_final_disputa) \
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

    def get_properties_order_by_address(self, wallet_id: str):
        with self.get_session_scope() as session:
            properties = session.query(
                Property.id.label('imovel_id'),
                Property.idr_imovel.label('idr'),
                Property.nome,
                Property.data_limite,
                Property.lote,
                Wallet.codigo,
                City.nome,
                City.estado,
                Address.bairro) \
                .select_from(Property) \
                .join(WalletProperty, Property.id == WalletProperty.imovel_id) \
                .join(Wallet, WalletProperty.carteira_id == Wallet.id) \
                .join(PropertyAddress, Property.id == PropertyAddress.imovel_id) \
                .join(Address, PropertyAddress.endereco_id == Address.id) \
                .join(City, Address.cidade_id == City.id) \
                .filter(Wallet.id == wallet_id).all()

            return properties

    def update_property(self, property_id: str, data: dict, history_data=None):
        with self.get_session_scope() as session:
            session.query(Property).\
                filter(Property.id == property_id).\
                update(data)

            if history_data:
                HistoryRepository().insert_property_history(imovel_id=property_id, fields=history_data)

        session.commit()

        
    def get_properties_wallet_to_leilao(self, wallet_id: str):
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
                Seller.nome.label('seller_name'),
                Property.idr_imovel,
                Manager.id.label('manager_id'),
                Manager.nome.label('manager_name'),
                Manager.url_whitelabel.label('gestor_url'),
                Schedule.id.label('schedule_id')) \
                .select_from(Wallet) \
                .join(WalletProperty, Wallet.id == WalletProperty.carteira_id) \
                .join(Property, WalletProperty.imovel_id == Property.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .join(WalletSchedule, Wallet.id == WalletSchedule.carteira_id) \
                .join(Schedule, WalletSchedule.cronograma_id == Schedule.id) \
                .join(SellerProperty, SellerProperty.imovel_id == Property.id, isouter=True) \
                .join(Seller, SellerProperty.vendedor_id == Seller.id, isouter=True) \
                .filter(Wallet.id == wallet_id,
                        and_(Schedule.data_inicio <= func.current_date(), Schedule.data_final >= func.current_date())) \
                .group_by(Property.id) \
                .order_by(func.abs(Property.lote)) 

            return transform_dict(properties)