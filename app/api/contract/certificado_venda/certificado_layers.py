from api.engine.document_interfaces import HTMLDocument, PDFLinkDocument
from api.contract.certificado_venda.certificado_templates import CertificadoVendaTemplate, CertificadoVendaRegulamentoTemplate, CertificadoVendaLogsTemplate


#####################################################################################
# --------------------------------- CERTIFICADO VENDA ------------------------------#

class CertificadoVendaCapa(CertificadoVendaTemplate, HTMLDocument):

    document_name = 'Certificado Venda - CAPA'
    current_layer = "capa.html"


class CertificadoVendaRegulamentoAprovado(CertificadoVendaRegulamentoTemplate, PDFLinkDocument):

    document_name = 'Regulamento Aprovado'

class CertificadoVendaLogsLayer(CertificadoVendaLogsTemplate):

    document_name = "Certificado Venda - LOGS"
    current_layer = []


# --------------------------------- CERTIFICADO VENDA ------------------------------#
#####################################################################################