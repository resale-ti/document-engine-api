from operator import attrgetter
from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.property_repository import PropertyRepository
from api.contract.certificado_venda.certificado_factory import CertificadoDocumentsFactory
from app.api.common.repositories.document_repository import DocumentRepository
from app.api.common.repositories.schedules_repository import SchedulesRepository
from app.api.contract.certificado_venda.certificado_library import CertificadoVendaLibrary
from app.api.contract.certificado_venda.certificado_facade import CertificadoVendaFacade
from app.api.contract.regulamento_concorrencia.regulamento_factory import RegulamentoDocumentsFactory

class CertificadoVendaBuilder(ContractBuilderBase):

    wallet_id = None
    document_id = None
    contract_base_name = "CertificadoVenda"
    stylesheet_path = "static/contracts_templates/certificado_venda/default-style.css"
    pagination = False
    property_id = None

    def __init__(self, data: dict) -> None:
        super().__init__()
        self.wallet_id = data.get("id_obj")

    def build(self) -> None:
        wallet, property, key = self.generate_property_sale_certificate()
        
        data = self.__get_data(wallet, property)
        
        documents_objects = self.__get_documents_objects_list(data)
    
    def generate_property_sale_certificate(self):

        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        if len(wallet) == 0:
            raise Exception("[ERROR]: Missing wallet_id")

        property = PropertyRepository().get_properties_wallet_with_disputa(self.wallet_id)

        if len(property) == 0:
            raise Exception("Imóvel não encontrado")

        key = CertificadoVendaLibrary.generate_new_key(wallet=wallet)

        # log.generate

        return wallet, property, key


    def __get_documents_objects_list(self, data):
        certificado_venda_factory = CertificadoDocumentsFactory(
        ).get_instance(self.wallet_id, data)
        
        regulamento = RegulamentoDocumentsFactory().get_instance(data.regulamento_url)
        
        certificado_venda_logs = "certificadovendalog"

        return certificado_venda_factory, regulamento, certificado_venda_logs
    
    
    def __get_data(self, wallet, property):
        
        schedule = SchedulesRepository.get_cronograma_carteira(self.wallet_id)
        
        regulamento_db = DocumentRepository.get_wallet_regulamento(self.wallet_id)
        
        for r in regulamento_db:
            if r == 'approved' or r == 'pending':
                abled_regulamento = r.documento_status
                
        last_regulamento = sorted(abled_regulamento, key=attrgetter('data_criacao'))
        
        # logs = 
        
        # sale_certificate_number = 
        
        certificado_venda_facade = CertificadoVendaFacade(
            wallet,
            schedule,
            property,
            last_regulamento
            # logs,
            # sale_certificate_number            
        )
        
        return certificado_venda_facade.parse()