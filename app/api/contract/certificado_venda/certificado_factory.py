from api.contract.certificado_venda.certificado_layers_default import CertificadoVendaLayerLogs, CertificadoCapa

class CertificadoDocumentsFactory:

    def get_instance(self, data):
        
        return [CertificadoVendaLayerLogs(data), CertificadoCapa(data)]