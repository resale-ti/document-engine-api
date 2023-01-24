from api.common.repositories.document_repository import DocumentRepository
from datetime import date, datetime
from utils.mail import Mail
import os


class RegulamentoConcorrenciaLibrary:

    def inactive_documents_from_wallet_id(self, wallet_id, document_id):
        regulamentos = DocumentRepository().get_wallet_regulamento(wallet_id=wallet_id)

        docs = []
        for regulamento in regulamentos:
            if regulamento.id != document_id:
                docs.append(regulamento.id)

        if len(docs) >= 1:
            DocumentRepository().inactive_many_documents(tuple(docs))

    def send_approved_document_email(self, wallet_id, document_id, doc_stream):
        regulamento = DocumentRepository().get_wallet_regulamento_approved(
            wallet_id=wallet_id, document_id=document_id)

        data_email = self._get_data_email(regulamento, doc_stream)

        mail = Mail(**data_email)
        mail.send_template_mail()

    def _get_data_email(self, regulamento, doc_stream) -> dict:
        template_name = "PGI-0025"
        subject = f"Regulamento Ativo - Melhor Proposta - {regulamento.disputa_id} - {regulamento.manager_name} - {date.today().strftime('%d/%m/%Y')}"

        if os.environ.get("STAGE").upper() == "PROD":
            to = [{'email': 'concorrencia@pagimovel.com.br'},
                  {'email': 'carteiras@pagimovel.com.br'}, {'email': 'homologacao@resale.com.br'}]
        else:
            # DEV OU LOCAL
            to = [{'email': 'dev.homologacao@resale.com.br'}]

        variables = [
            {"name": "NOME_GESTOR", "content": regulamento.manager_name},
            {"name": "ID_CARTEIRA", "content": regulamento.codigo},
            {"name": "NOME_disputa", "content": regulamento.wallet_name},
            {"name": "DATA_HORA", "content": datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]

        attachments = [{"type": "application/pdf",
                        "name": regulamento.documento_nome,
                        "content": doc_stream.decode('utf-8')}]

        return {
            "template_name": template_name,
            "to": to,
            "subject": subject,
            "variables": variables,
            "from_name": 'Pagimovel',
            "from_email": 'contato@pagimovel.com.br',
            "attachments": attachments
        }
