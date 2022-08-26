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
metadata.reflect(engine, only=['tarefas_celery', 
                               'imovel', 
                               'carteira_imovel', 
                               'carteira', 
                               'imovel_history', 
                               'carteira_history', 
                               'oportunidade',
                               'oportunidade_imovel',
                               'ci_sessions', 
                               'usuario'
                               ])

Base = automap_base(metadata=metadata)
