from api.contract.certificado_venda.certificado_layers import CertificadoCapa, CertificadoRodape

class CertificadoDocumentsFactory:

    def get_instance(self, property_id, data):
        
        return [CertificadoCapa(property_id, data), CertificadoRodape(property_id, data)]