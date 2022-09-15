from fastapi import APIRouter
from api.contract.contract import Contract
from api.contract.schemas import ContractBaseSchema
from api.contract.contract_enum import EnumContractType
import traceback
import sys



router = APIRouter()

@router.post('/contract-generate')
async def generate_fastapi(payload: ContractBaseSchema):
    try:
        contract_type = payload.contract_type

        if contract_type not in [ct.value for ct in EnumContractType]:
            raise Exception("Insert a valid type of ContractType.")

        Contract.generate_contract(contract_type=contract_type, data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}
