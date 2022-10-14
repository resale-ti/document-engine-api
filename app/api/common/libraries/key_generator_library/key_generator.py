from api.common.libraries.key_generator_library.key_generator_factory import KeyGeneratorFactory


class KeyGenerator:

    def generate_key(data: dict) -> None:
        key_generator_factory = KeyGeneratorFactory().get_instance(data)
        
        return key_generator_factory