from fastapi import APIRouter, status, Response
from api.contract.contract import Contract

from utils.rollbar_handler import response_rollbar_handler

from api.engine.builder import BuilderEngine

from pathlib import Path
from datetime import datetime
import os
BASE_DIR = Path(__file__).resolve().parent.parent.parent
template_path = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')


router = APIRouter()

def get_html_template(html_filename):
    return Path(os.path.join(template_path + '/CEM001_002', html_filename)).read_text()

@router.get('/teste')
async def teste():
    html_template_titulo= get_html_template('titulo-layer.html')
    html_template_imovel = get_html_template('imovel-layer.html')
    default_style = os.path.join(template_path, 'regulamento.css')
    filename = 'regulamento.pdf'

    titulo_data = {"NUMERO_PROPOSTA": "1234"}
    imovel_data = {"IDR": "1234", "ID_BANCO": "54321", "IMOVEL": "wesley"}

    html = BuilderEngine.render(data=titulo_data, html=html_template_titulo)
    html += BuilderEngine.render(data=imovel_data, html=html_template_imovel)

    file_bytes = BuilderEngine.generate_pdf_byte(html=html, default_style=default_style)

    return {"status": "200"}

############################################################################################
############################################################################################
############################################################################################

@router.get('/{contract_type}/{id}')
async def generate(contract_type: str, id: str):
    result = Contract.generate_contract(contract_type=contract_type, data={"wallet_id": id})
    print("alo galera de cowboy")
    return {"status": 200}



