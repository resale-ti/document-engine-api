from fastapi import APIRouter
from api.contract.contract import Contract
from api.contract.schemas import RegulamentoSchema, CertificadoVendaSchema
from api.common.repositories.property_repository import PropertyRepository
from utils.wuzu.auctions import Auctions
from api.contract.regulamento_concorrencia.regulamento_conditions import ConditionsRegulamento

import traceback
import sys
import os



router = APIRouter()

@router.post('/regulamento-concorrencia-completo')
async def generate_regulamento_and_cv(payload: RegulamentoSchema):
    try:
        carteira_id = payload.id_obj
        os.environ["REQUESTER_ID"] = payload.requester_id
        os.environ["DOCUMENT_ID_RC"] = ""

        # Handled das auctions na Wuzu.
        # Auctions().handle_auctions(dict(payload))

        cond_regulamento = ConditionsRegulamento(payload=dict(payload))
        cond_regulamento.execute_pre_conditions()

        # Geração do Regulamento
        Contract.generate_contract(contract_type="regulamento_concorrencia", data=dict(payload))

        properties = PropertyRepository().get_properties_wallet_with_schedule(wallet_id=carteira_id)

        for prop in properties:
            data = {"id_obj": carteira_id, "property_id": prop.imovel_id}
            Contract.generate_contract(contract_type="certificado_venda", data=data)

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}


@router.post('/regulamento-concorrencia')
async def generate_regulamento(payload: RegulamentoSchema):
    try:
        # Geração do Regulamento
        Contract.generate_contract(contract_type="regulamento_concorrencia", data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}


@router.post('/certificado-venda')
async def generate_cv(payload: CertificadoVendaSchema):
    try:
        Contract.generate_contract(contract_type="certificado_venda", data=dict(payload))

        return {"status": 200}

    except Exception as err:
        print(traceback.format_exc())
        print(sys.exc_info()[2])
        return {"status": 400, "error": str(err)}
