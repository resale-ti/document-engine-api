from abc import ABC, abstractmethod

class ContractBuilderInterface(ABC):

    @abstractmethod
    def build(self):
        pass


class ContractFacadeInterface(ABC):

    @abstractmethod
    def parse(self):
        pass
