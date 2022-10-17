from select import select
from api.common.database_common import DBSessionContext
from api.common.models import Wallet, Schedule, WalletSchedule
from sqlalchemy import func, and_

class SchedulesRepository(DBSessionContext):
    
    def get_cronograma_carteira(self, wallet_id):
        with self.get_session_scope() as session:
            schedule = session.query(
                    Schedule.nome
                )\
                .select_from(Schedule) \
                .join(WalletSchedule, Schedule.id == WalletSchedule.cronograma_id) \
                .join(Wallet, WalletSchedule.carteira_id == Wallet.id) \
                .filter(Wallet.id == wallet_id,
                        and_(Schedule.data_inicio <= func.current_date(), Schedule.data_final >= func.current_date())).all()

            return schedule