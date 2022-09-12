from app.api.contract.contract_factory import ContractFactory


class Contract:

    def generate_contract(contract_type: str, data: dict):
        contract = ContractFactory().get_instance(contract_type=contract_type, data=data)

        contract.build()

        return "123"