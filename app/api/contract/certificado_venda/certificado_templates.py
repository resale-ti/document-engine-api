from mimetypes import init
import os
from re import template
from api.contract.certificado_venda import PATH_CERTIFICADO_FOLDER
from api.contract.contract_builder_interface import ContractBuilderInterface
from api.contract.certificado_venda.certificado_layers import CertificadoVendaLogsTitulo, CertificadoVendaLogsBody

class CertificadoVendaTemplate(ContractBuilderInterface):
    
    template_path = PATH_CERTIFICADO_FOLDER
    stylesheets = 'certificado_venda.css'
    
    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data
    
    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes
    
    
class CertificadoVendaRegulamentoTemplate(ContractBuilderInterface):
    
    template_path = PATH_CERTIFICADO_FOLDER
    stylesheets = 'certificado_venda.css'
    
    def __init__(self, url_regulamento) -> None:
        self.url_layer = url_regulamento
        
    def build(self, engine):
        file_bytes = engine._handle_with_instances(self)
        return file_bytes
    

class CertificadoVendaLogsTemplate(ContractBuilderInterface):
    
    template_path = PATH_CERTIFICADO_FOLDER
    stylesheets = 'certificado_venda.css'
    
    def __init__(self, wallet_id, data) -> None:
        self.wallet_id = wallet_id
        self.data = data
        
    def instance_layers(self):
        current_layer = []
        
        current_layer.append(CertificadoVendaLogsTitulo())
        
        for logs in self.data.get('LOGS'):
            current_layer.append(CertificadoVendaLogsBody(logs))
        
        return current_layer
    
    def build(self, engine):
        html = ""
        self.current_layer = self.instance_layers()

        for document in self.current_layer:
            html += engine._generate_html_with_data(document)

        default_style = os.path.join(self.template_path, self.stylesheets)

        return engine.generate_pdf_byte(html=html, default_style=default_style)
        
        