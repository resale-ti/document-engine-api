from abc import ABC, abstractmethod

class ContractBuilderInterface(ABC):

    @abstractmethod
    def build(self):
        pass