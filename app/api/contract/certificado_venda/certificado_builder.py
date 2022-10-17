from api.contract.contract_builder_base import ContractBuilderBase
from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.property_repository import PropertyRepository
from api.contract.certificado_venda.certificado_factory import CertificadoDocumentsFactory
from app.api.contract.certificado_venda.certificado_library import CertificadoVendaLibrary

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

        data = self.__get_data()

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
        ).get_instance(self.property_id, data)

        return certificado_venda_factory