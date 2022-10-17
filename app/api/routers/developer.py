from fastapi import APIRouter
from api.contract.contract import Contract
from api.contract.schemas import ContractBaseSchema, RegulamentoSchema
from api.contract.contract_enum import EnumContractType
from utils.wuzu.auctions import Auctions

import traceback
import sys



router = APIRouter()

@router.post('/regulamento-concorrencia')
async def generate_fastapi(payload: RegulamentoSchema):
    try:
        # Handled das auctions na Wuzu.
        # Auctions(task_progress=progressbar).handle_auctions(dict(payload))

        # Geração do Regulamento
        Contract.generate_contract(contract_type="regulamento_concorrencia", data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}


@router.post('/certificado-venda')
async def generate_fastapi(payload: ContractBaseSchema):
    try:
        Contract.generate_contract(contract_type="certificado_venda", data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}
