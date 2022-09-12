from fastapi import APIRouter, status, Response
from api.contract.contract import Contract

from utils.rollbar_handler import response_rollbar_handler

router = APIRouter()

@router.get('/{contract_type}/{id}')
async def generate(contract_type: str, id: str):
    result = Contract.generate_contract(contract_type=contract_type, data={"wallet_id": id})
    return {"status": 200}



