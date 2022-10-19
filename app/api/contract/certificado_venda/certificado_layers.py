from api.engine.document_interfaces import HTMLDocument, PDFLinkDocument
from api.contract.certificado_venda import PATH_CERTIFICADO_FOLDER
from api.contract.certificado_venda.certificado_templates import CertificadoVendaTemplate, CertificadoVendaRegulamentoTemplate, CertificadoVendaLogsTemplate


#####################################################################################
# --------------------------------- CERTIFICADO VENDA ------------------------------#

class CertificadoCapa(CertificadoVendaTemplate, HTMLDocument):
    
    document_name = 'Certificado Venda - CAPA' 
    current_layer = "capa.html"
    

class CertificadoVendaRegulamentoAprovado(CertificadoVendaRegulamentoTemplate, PDFLinkDocument):

    document_name = 'Regulamento Aprovado'


class CertificadoVendaLogsTitulo(CertificadoVendaLogsTemplate, HTMLDocument):
    
    template_path = PATH_CERTIFICADO_FOLDER
    document_name = 'Certificado Venda Logs- Titulo'
    current_layer = 'certificado_venda_logs_titulo.html'
    

class CertificadoVendaLogsBody(CertificadoVendaLogsTemplate, HTMLDocument):
    
    template_path = PATH_CERTIFICADO_FOLDER
    document_name = 'Certificado Venda Logs'
    current_layer = 'certificado_venda_logs_body.html'
    
    def __init__(self, logs) -> None:
        self.data = logs
    
# --------------------------------- CERTIFICADO VENDA ------------------------------#
#####################################################################################