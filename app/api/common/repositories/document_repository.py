from api.common.database_common import DBSessionContext
from api.common.models import Document, WalletDocument, Wallet, WalletManager, Manager, DocumentRevision
from sqlalchemy import or_, update


class DocumentRepository(DBSessionContext):

    def get_wallet_regulamento(self, wallet_id: str):

        with self.get_session_scope() as session:
            regulamentos = session.query(Document.id) \
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