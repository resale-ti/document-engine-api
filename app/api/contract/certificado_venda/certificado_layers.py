from api.engine.document_interfaces import HTMLDocument, PDFDocument
from api.contract.certificado_venda.certificado_templates import CertificadoVenda, CertificadoVendaRodapeDefault


#####################################################################################
# ------------------------------------- MLP002 -------------------------------------#

class CertificadoCapa(CertificadoVenda, HTMLDocument):

    document_name = "Certificado Venda - CAPA"
    current_layer = "capa.html"


class CertificadoRodape(CertificadoVendaRodapeDefault):

    document_name = "Certificado Venda - RODAPÉ"
    stylesheets = "certificado_venda.css"
    current_layer = []

# ------------------------------------- MLP002 -------------------------------------#
#####################################################################################