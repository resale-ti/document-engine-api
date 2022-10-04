from api.contract.certificado_venda.certificado_layers import CertificadoCapa, CertificadoRodape

class CertificadoDocumentsFactory:

    def get_instance(self, wallet_id, data):
        
        return [CertificadoCapa(wallet_id, data), CertificadoRodape(wallet_id, data)]