from datetime import date
from api.common.libraries.key_generator_library.key_generator_interface import KeyGeneratorBuildInterface
from api.common.libraries.key_generator_library.key_generator_enum import PrefixKeyGenertorBuildEnum
from app.api.common.repositories.document_repository import DocumentRepository


class KeyGeneratorBuilder(KeyGeneratorBuildInterface):
    
    def __init__(self, data: dict) -> None:
        super().__init__()
        
        self.year = date("%Y")
        self.data = data
        self.__str_pag_length = 7
        
    def generate(self) -> None:
        
        prefix = self.get_prefix()
        
        middle = self.get_middle()
        
        posfix = self.get_sequential
        
        return f"{prefix}{middle}{posfix}"
    
    def get_prefix():
        pass
    

class CertificadoVenda(KeyGeneratorBuilder):
    
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.__str_pag_length = 7
        self.__prefix = PrefixKeyGenertorBuildEnum.CERTIFICADO_VENDA.value
        
    def generate(self) -> None:
        prefix = KeyGeneratorBuilder.get_prefix()
        middle = self.get_middle()
        posfix = self.get_sequential()
        
        return f"{prefix}{middle}{posfix}"
    
    def get_sequential(self):
        str_pag_length = self.__str_pag_length
        
        last_certificado_venda_db = DocumentRepository.get_last_certificado_venda(
            self.__prefix, 
            self.year, 
            PrefixKeyGenertorBuildEnum.CONCORRENCIA_PUBLICA.value,
            str_pag_length
        )
        
        last_sequential = last_certificado_venda_db.sequential if last_certificado_venda_db else 0
        
        next_sequential = int(last_sequential) + 1
        
        return 
    
    def get_middle():
        numero_concorrencia = CertificadoVenda.get_concorrencia_publica()
        return numero_concorrencia
    
    def get_concorrencia_publica(self):
       
       data = self.data
       
       if "concorrencia_publica" in data.keys() == False:
           raise Exception("Número da disputa digital não encontrado")
       
       concorrencia_publica = data.concorrencia_publica
       
       return concorrencia_publica
       
    
        