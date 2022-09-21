from fastapi import APIRouter
from api.contract.contract import Contract
from api.contract.schemas import ContractBaseSchema, RegulamentoSchema
from api.contract.contract_enum import EnumContractType
import traceback
import sys



router = APIRouter()

@router.post('/regulamento-concorrencia')
async def generate_fastapi(payload: RegulamentoSchema):
    try:
        Contract.generate_contract(contract_type="regulamento_concorrencia", data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}
