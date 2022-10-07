from api.contract.regulamento_concorrencia.regulamento_builder import RegulamentoConcorrenciaBuilder
from api.contract.edital.edital_builder import EditalBuilder 
from api.contract.contract_enum import EnumContractType

class ContractFactory:

    @staticmethod
    def get_instance(contract_type: str, data: dict):
        contract_builder_class = None

        if contract_type == EnumContractType.REGULAMENTO_CONCORRENCIA.value:
            contract_builder_class = RegulamentoConcorrenciaBuilder(data=data)
        elif contract_type == EnumContractType.EDITAL.value:
            contract_builder_class = EditalBuilder(data=data)
        else:
            raise('ffff')

        return contract_builder_class