from api.common.libraries.key_generator_library.key_generator_enum import KeyGeneratorEnum
from api.common.libraries.key_generator_library.key_generator_builder import CertificadoVenda, KeyGeneratorBuilder

class KeyGeneratorFactory:
    
    def get_instance(data: dict):
        
        key_generator_class = None
        
        key_generator = data.tipo
        
        if key_generator == KeyGeneratorEnum.CERTIFICADO_VENDA.value:
            key_generator_class = CertificadoVenda(data=data)
            
        return key_generator_class