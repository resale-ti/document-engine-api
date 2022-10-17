from api.contract.certificado_venda.certificado_layers import CertificadoCapa, CertificadoRodape

class CertificadoDocumentsFactory:

    def get_instance(self, walllet_id, data):
        
        return [CertificadoCapa(walllet_id, data), CertificadoRodape(walllet_id, data)]