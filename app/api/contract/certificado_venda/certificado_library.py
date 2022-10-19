from api.common.libraries.key_generator_library.key_generator_enum import KeyGeneratorEnum
from api.common.libraries.key_generator_library.key_generator import KeyGenerator


class CertificadoVendaLibrary:

    @staticmethod
    def generate_new_key(wallet: dict):
        data = {'tipo': KeyGeneratorEnum.CERTIFICADO_VENDA.value,
                'concorrencia_publica': wallet.disputa_id}

        key = KeyGenerator.generate_key(data)

        return key


