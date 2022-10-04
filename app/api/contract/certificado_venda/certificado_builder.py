from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.seller_repository import SellerRepository
from api.common.repositories.property_repository import PropertyRepository
from api.common.repositories.qualification_repository import QualificationRepository
from api.common.repositories.property_auction_repository import PropertyAuctionRepository
from api.common.repositories.manager_repository import ManagerRepository
from api.contract.certificado_venda.certificado_factory import CertificadoDocumentsFactory
# from api.contract.certificado_venda.certificado_facade import
# from api.contract.certificado_venda.certificado_library import C
# from api.contract.certificado_venda.certificado_helpers import
from utils.admin_integrations.documents import AdminAPIDocuments
from utils.admin_integrations.wallets import AdminAPIWallets
import time
from datetime import date

class CertificadoVendaBuilder(ContractBuilderBase):
    
    def build(self) -> None:
        return self