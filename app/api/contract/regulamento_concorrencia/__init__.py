from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PATH_REGULAMENTO_FOLDER = os.path.join(BASE_DIR, 'static', 'templates', 'regulamento_concorrencia')
