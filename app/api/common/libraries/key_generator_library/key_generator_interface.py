from abc import ABC, abstractmethod

class KeyGeneratorBuildInterface(ABC):
    
    @abstractmethod
    def get_prefix():
        pass
    
    @abstractmethod
    def get_middle():
        pass
    
    @abstractmethod
    def get_sequential():
        pass
    
    @abstractmethod
    def generate():
        pass