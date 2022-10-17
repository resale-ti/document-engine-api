from api.common.database_common import DBSessionContext
from api.common.models import CertificadoVendaLogs
import uuid


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

    def add_log(self, data: dict):
        with self.get_session_scope() as session:
            logs = CertificadoVendaLogs(
                imovel_id=data.get("imovel_id"),
                carteira_id=data.get("carteira_id"),
                descricao=data.get("descricao"),
                data_criacao=data.get("data_criacao"))

            session.add(logs)
