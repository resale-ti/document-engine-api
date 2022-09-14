from fastapi import APIRouter
from api.contract.contract import Contract
from api.contract.schemas import ContractSchema
from api.contract.contract_enum import EnumContractType


router = APIRouter()

@router.post('/contract-generate')
async def generate_fastapi(payload: ContractSchema):
    try:
        contract_type = payload.contract_type

        if contract_type not in [ct.value for ct in EnumContractType]:
            raise Exception("Insert a valid type of ContractType.")

        data = {"id_obj": payload.id_obj}

        Contract.generate_contract(contract_type=contract_type, data=data)

        return {"status": 200}
    except Exception as err:
        return {"status": 400, "error": str(err)}
