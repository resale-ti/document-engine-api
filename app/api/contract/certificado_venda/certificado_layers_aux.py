from api.engine.document_interfaces import HTMLDocument
from api.contract.certificado_venda import PATH_CERTIFICADO_FOLDER


class CertificadoVendaLogsTitulo(HTMLDocument):

    template_path = PATH_CERTIFICADO_FOLDER
    document_name = 'Certificado Venda Logs- Titulo'
    current_layer = 'certificado_venda_logs_titulo.html'


class CertificadoVendaLogsBody(HTMLDocument):

    template_path = PATH_CERTIFICADO_FOLDER
    document_name = 'Certificado Venda Logs'
    current_layer = 'certificado_venda_logs_body.html'

    def __init__(self, logs) -> None:
        self.data = logs