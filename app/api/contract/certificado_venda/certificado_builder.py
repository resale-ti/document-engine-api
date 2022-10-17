from unittest import result
from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.seller_repository import SellerRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.common.repositories.sales_certificate_repository import SalesCertificateRepository
from api.contract.certificado_venda.certificado_factory import CertificadoDocumentsFactory
from app.api.contract.certificado_venda.certificado_library import CertificadoVendaLibrary
from app.utils.admin_integrations.property import AdminAPIProperty
# from api.contract.certificado_venda.certificado_facade import CertificadoVendaFacade
# from api.contract.certificado_venda.certificado_library import CertificadoVendaFactory
# from api.contract.certificado_venda.certificado_helpers import CertificadoVendaLibrary
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.wallets import AdminAPIWallets
from api.task_control.progressbar import TaskProgress
from api.common.libraries.key_generator_library.key_generator_builder import KeyGeneratorBuilder
from api.common.libraries.key_generator_library.key_generator_builder import CertificadoVenda
from api.common.libraries.key_generator_library.key_generator import KeyGenerator

import time
from datetime import date

class CertificadoVendaBuilder(ContractBuilderBase):
    
    wallet_id = None
    document_id = None
    contract_base_name = "CertificadoVenda"
    stylesheet_path = "static/contracts_templates/certificado_venda/default-style.css"
    pagination = False
    property_id = None

    def __init__(self, data: dict) -> None:
        super().__init__()

        if not "wallet_id" in data:
            raise Exception("[ERROR]: Missing wallet_id")
        
        if not "property_id" in data:
            raise Exception("[ERROR]: Missing property_id")

        self.wallet_id = data.wallet_id
        self.property_id = data.property_id
        
    def build(self) -> None:
        
        wallet, property, key = self.generate_property_sale_certificate()
        
        data = self.__get_data()
        
        
    
    
    def generate_property_sale_certificate(self):
        
        wallet = WalletRepository().get_wallet_details(self.wallet_id)
        if len(wallet) == 0:
            raise Exception("[ERROR]: Missing wallet_id")
        
        property = PropertyRepository().get_properties_wallet(self.wallet_id)
        
        if len(property) == 0:
            raise Exception("Imóvel não encontrado")
        
        key = CertificadoVendaLibrary.generate_new_key(wallet)
        
        # log.generate
        
        return wallet, property, key
        
        
    def __get_documents_objects_list(self, data):
        certificado_venda_factory = CertificadoDocumentsFactory(
        ).get_instance(self.property_id, data)

        return certificado_venda_factory