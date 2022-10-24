from api.common.libraries.key_generator_library.key_generator_factory import KeyGeneratorFactory


class KeyGenerator:

    @staticmethod
    def generate_key(data: dict) -> None:
        key_generator_factory = KeyGeneratorFactory.get_instance(data)
        
        key = key_generator_factory.generate()

        return key