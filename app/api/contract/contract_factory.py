from api.contract.regulamento_concorrencia.regulamento_builder import RegulamentoConcorrenciaBuilder
from api.contract.certificado_venda.certificado_builder import CertificadoVendaBuilder
from api.contract.contract_enum import EnumContractType

class ContractFactory:

    @staticmethod
    def get_instance(contract_type: str, data: dict):
        contract_builder_class = None

        if contract_type == EnumContractType.REGULAMENTO_CONCORRENCIA.value:
            contract_builder_class = RegulamentoConcorrenciaBuilder(data=data)
        elif contract_type == EnumContractType.CERTIFICADO_VENDA.value:
            contract_builder_class = CertificadoVendaBuilder(data=data)
        return contract_builder_class