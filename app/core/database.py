from curses import echo
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
import os

DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASS = os.environ.get('DATABASE_PASS')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# produce our own MetaData object
metadata = MetaData()

# we can reflect it ourselves from a database, using options
# such as 'only' to limit what tables we look at...
metadata.reflect(engine, only=['imovel', 'carteira_imovel', 'qualificacao', 'carteira', 'carteira_cronograma', 'cronograma',
                               'tarefas_celery', 'carteira_gestor', 'gestor', 'disputa_wuzu', 'carteira_formas_pagamento',
                               'carteira_condicoes_pagamento', 'carteira_parcelas', 'documento', 'imovel_endereco', 'endereco',
                               'documento_revisao', 'carteira_documento', 'usuario', 'certificados_venda_logs', 'cidade',
                               'imovel_history', 'carteira_history'])

Base = automap_base(metadata=metadata)
