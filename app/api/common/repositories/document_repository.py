from api.common.database_common import DBSessionContext
from api.common.models import Document, WalletDocument, Wallet, WalletManager, Manager, DocumentRevision
from sqlalchemy import or_, update
from sqlalchemy import func, desc, cast, Numeric


class DocumentRepository(DBSessionContext):

    def get_wallet_regulamento(self, wallet_id: str):

        with self.get_session_scope() as session:
            regulamentos = session.query(
                    Document.id,
                    Document.documento_status,
                    Document.data_criacao,
                    Document.revisao_documento_id
                ) \
                .join(WalletDocument, Document.id == WalletDocument.documento_id) \
                .join(Wallet, WalletDocument.carteira_id == Wallet.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .filter(or_(Document.documento_status == None, Document.documento_status != "deleted"),
                        Wallet.id == wallet_id,
                        Document.categoria_id == "regulamento") \
                .order_by(Document.data.desc()).all()

            return regulamentos

    def inactive_many_documents(self, docs: tuple) -> None:
        with self.get_session_scope() as session:
            inactive = session.execute(update(Document).
                                       where(Document.id.in_(docs)).
                                       values(documento_status='inactive'))

    def failed_regulamento(self, document_id: str) -> None:
        with self.get_session_scope() as session:
            failed = session.execute(update(Document).
                                       where(Document.id == document_id).
                                       values(documento_status='failed'))


    def get_document_revision(self, document_id):
        with self.get_session_scope() as session:
            doc_revision = session.query(DocumentRevision.id) \
                            .join(Document, Document.id == DocumentRevision.documento_id) \
                            .filter(Document.id == document_id).one()

            return doc_revision

    def get_wallet_regulamento_approved(self, wallet_id, document_id):
        with self.get_session_scope() as session:
            regulamento_approved = session.query(Document.id,
                                                 Wallet.disputa_id,
                                                 Manager.nome.label("manager_name"),
                                                 Wallet.nome.label("wallet_name"),
                                                 Wallet.codigo,
                                                 Document.documento_nome) \
                .join(WalletDocument, Document.id == WalletDocument.documento_id) \
                .join(Wallet, WalletDocument.carteira_id == Wallet.id) \
                .join(WalletManager, Wallet.id == WalletManager.carteira_id) \
                .join(Manager, WalletManager.gestor_id == Manager.id) \
                .filter(or_(Document.documento_status == None, Document.documento_status == "approved"),
                        Wallet.id == wallet_id,
                        Document.id == document_id,
                        Document.categoria_id == "regulamento").one()

            return regulamento_approved

    def get_active_regulamento_wallet(self, wallet_id: str):

        with self.get_session_scope() as session:
            regulamento_ativo = session.query(Document.id, Document.revisao_documento_id) \
                .join(WalletDocument, Document.id == WalletDocument.documento_id) \
                .join(Wallet, WalletDocument.carteira_id == Wallet.id) \
                .filter(Document.documento_status == "approved",
                        Wallet.id == wallet_id,
                        Document.categoria_id == "regulamento") \
                .one()

            return regulamento_ativo

    def get_last_certificado_venda(self, prefix, length):
        with self.get_session_scope() as session:
            certificado_venda = session.query(
                Document.numero_certificado_venda,
                cast(func.substr(Document.numero_certificado_venda, -length, length), Numeric()).label("sequential")) \
                .filter(Document.numero_certificado_venda != None,
                        Document.numero_certificado_venda != '',
                        Document.numero_certificado_venda.like(prefix)) \
                .order_by(desc("sequential")).first()

            return certificado_venda