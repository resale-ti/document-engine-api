import mailchimp_transactional as MailchimpTransactional
from datetime import datetime
import os

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

MAILCHIMP_API_KEY = "OI1VfXftZJyq73X7Xh1czQ"
mailchimp = MailchimpTransactional.Client(MAILCHIMP_API_KEY)


class Mail(object):
    def __init__(self, **kwargs):
        self.subject = self.get_subject_by_stage(kwargs.get('subject'))
        self.to = self.get_recipient_by_stage(kwargs.get('to'))
        self.cc = self.get_copy_recipient_by_stage(
            kwargs.get('cc', "tec@resale.com.br"))
        self.from_email = kwargs.get('from_email')
        self.from_name = kwargs.get('from_name')
        self.template_name = kwargs.get('template_name')
        self.variables = kwargs.get('variables')
        self.attachments = kwargs.get('attachments')
        self.template_contente = [{"name": "xxxx", "content": "xxx"}]

    def send_template_mail(self) -> None:
        """
        Envia o modelo do e-mail.
        """
        mailchimp.messages.send_template({"template_name": self.template_name,
                                          "template_content": self.template_contente,
                                          "message": self.get_message()})

    def get_message(self) -> dict:
        """
        Obtem as informações do e-mail do contato.
        @return: dict com os dados.
        """
        return {
            "attachments": self.attachments,
            "from_email": self.from_email,
            "from_name": self.from_name,
            "to": self.to,
            "bcc_address": self.cc,
            "subject": self.subject,
            "html": "",
            "text": "",
            "merge_language": "mailchimp",
            "global_merge_vars": self.variables,
        }

    @staticmethod
    def get_copy_recipient_by_stage(copy_recipient: str) -> str:
        """
        Obtem em qual stage a aplicação está rodando. Dev ou Prod.
        @param copy_recipient:
        @return: str com
        """
        return os.environ.get("DEV_EMAIL") if os.environ.get("STAGE").upper() == "DEV" else copy_recipient

    @staticmethod
    def get_subject_by_stage(subject):
        """
        Obtem o assunto do e-mail verificando o stage que esteja, ou seja, dev ou prod.
        @param subject:
        @return:
        """
        return f"HOMOLOG:{subject}" if os.environ.get("STAGE").upper() == "DEV" else subject

    @staticmethod
    def get_recipient_by_stage(recipient: str) -> list:
        """
        Obtem o destinatário verificando se está em dev ou prod.
        @param recipient: str com os dados caso não esteja em dev.
        @return: list com o e-mail de envio.
        """
        return [{"email": "dev.homologacao@resale.com.br"}, recipient] if os.environ.get("STAGE").upper() == "DEV" else recipient
