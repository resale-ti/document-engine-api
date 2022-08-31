from api.contract.regulamento_concorrencia.regulamento_builder import RegulamentoConcorrenciaBuilder
from api.contract.contract_enum import EnumContractType

class ContractFactory:

    @staticmethod
    def get_instance(contract_type: str, data: dict):
        contract_builder_class = None

        if contract_type == EnumContractType.REGULAMENTO_CONCORRENCIA.value:
            contract_builder_class = RegulamentoConcorrenciaBuilder(data=data)

        return contract_builder_class