from api.common.database_common import DBSessionContext
from api.common.models import DisputaWuzu
from app.api.common.helpers import transform_dict


class PropertyAuctionRepository(DBSessionContext):
    def get_wuzu_auction_id_by_property_id_from_property_auction(self, property_id: str, schedule_id: str):
        with self.get_session_scope() as session:
            wuzu_action = session.query(DisputaWuzu.wuzu_disputa_id.label('wuzu_auction_id'),
                                        DisputaWuzu.data_inicio_disputa.label('date_start_auction'),
                                        DisputaWuzu.data_final_disputa.label('date_finish_auction'),
                                        DisputaWuzu.wuzu_status) \
                .filter(DisputaWuzu.imovel_id == property_id,
                        DisputaWuzu.cronograma_id == schedule_id,
                        DisputaWuzu.wuzu_status.not_in(('canceled', 'closed'))) \
                .order_by(DisputaWuzu.id.desc()).one()

            return wuzu_action
