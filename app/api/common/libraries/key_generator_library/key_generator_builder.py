from datetime import datetime
from abc import abstractmethod
from api.common.libraries.key_generator_library.key_generator_interface import KeyGeneratorBuildInterface
from api.common.libraries.key_generator_library.key_generator_enum import PrefixKeyGenertorBuildEnum
from api.common.repositories.document_repository import DocumentRepository


class KeyGeneratorBuilder(KeyGeneratorBuildInterface):

    def __init__(self, data: dict) -> None:
        super().__init__()

        self.year = datetime.now().year
        self.data = data

    def generate(self):
        prefix = self.get_prefix()
        middle = self.get_middle()
        posfix = self.get_sequential()

        return f"{prefix}-{middle}-{posfix}"

    @abstractmethod
    def get_prefix(self):
        pass

    @abstractmethod
    def get_middle(self):
        pass

    @abstractmethod
    def get_sequential(self):
        pass


class CertificadoVendaKey(KeyGeneratorBuilder):

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.__str_pag_length = 7
        self.__prefix = PrefixKeyGenertorBuildEnum.CERTIFICADO_VENDA.value

    def get_prefix(self):
        return self.__prefix

    def get_middle(self):
        numero_concorrencia = self.__get_concorrencia_publica()
        return numero_concorrencia

    def get_sequential(self):
        str_pag_length = self.__str_pag_length

        where_prefix = f'{self.__prefix}-{PrefixKeyGenertorBuildEnum.CONCORRENCIA_PUBLICA.value}{self.year}%'

        last_certificado_venda_db = DocumentRepository().get_last_certificado_venda(prefix=where_prefix, length=str_pag_length)

        last_sequential = last_certificado_venda_db.sequential if last_certificado_venda_db else 0

        next_sequential = str(int(last_sequential) + 1)

        return next_sequential.zfill(str_pag_length)

    def __get_concorrencia_publica(self):
       if "concorrencia_publica" in self.data.keys() == False:
           raise Exception("Número da disputa digital não encontrado")

       concorrencia_publica = self.data.get("concorrencia_publica")

       return concorrencia_publica


