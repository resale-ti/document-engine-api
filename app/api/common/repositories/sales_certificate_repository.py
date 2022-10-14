from api.common.database_common import DBSessionContext
from api.common.models import CertificadoVendaLogs


class SalesCertificateRepository(DBSessionContext):
    def get_sales_certificate(self, property_id: str):
        with self.get_session_scope() as session:
            sales_certificate = session.query(
                CertificadoVendaLogs.id,
                CertificadoVendaLogs.data_criacao,
                CertificadoVendaLogs.imovel_id,
                CertificadoVendaLogs.carteira_id,
                CertificadoVendaLogs.descricao
            ).filter(CertificadoVendaLogs.imovel_id == property_id).one()

            return sales_certificate