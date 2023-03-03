import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.path.isfile(os.path.join(BASE_DIR, '.env')):
    load_dotenv()

broker_url = os.environ.get('BROKER_URL')

RESULT_BACKEND_HOST = os.environ.get('RESULT_BACKEND_HOST')
RESULT_BACKEND_NAME = os.environ.get('RESULT_BACKEND_NAME')
RESULT_BACKEND_USER = os.environ.get('RESULT_BACKEND_USER')
RESULT_BACKEND_PASS = os.environ.get('RESULT_BACKEND_PASS')

result_backend = f"db+mysql://{RESULT_BACKEND_USER}:{RESULT_BACKEND_PASS}@{RESULT_BACKEND_HOST}/{RESULT_BACKEND_NAME}"

result_persistent = True
result_exchange = 'celery_result'
result_exchange_type = 'direct'
task_track_started = True
