from api.common.repositories.wallet_repository import WalletRepository
from api.common.repositories.document_repository import DocumentRepository
from api.common.libraries.key_generator_library.key_generator_enum import KeyGeneratorEnum
from api.common.libraries.key_generator_library.key_generator import KeyGenerator
import os


class CertificadoVendaLibrary:
    
    def generate_new_key(self, wallet):
        
        data = {
            'tipo': KeyGeneratorEnum.CERTIFICADO_VENDA.value,
            'concorrencia_publica': wallet.disputa_id
        }
        
        key = KeyGenerator.generate_key(data)
        
        return key
        
        
