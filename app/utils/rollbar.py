import rollbar
import os

from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.path.isfile(os.path.join(BASE_DIR, '.env')):
    load_dotenv()

rollbar.init(os.environ.get("ROLLBAR_KEY"),
             environment=os.environ.get("STAGE"))
