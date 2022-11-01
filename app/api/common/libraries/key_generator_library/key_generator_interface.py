from abc import ABC, abstractmethod

class KeyGeneratorBuildInterface(ABC):

    @abstractmethod
    def generate():
        pass