from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
PATH_CERTIFICADO_FOLDER = os.path.join(BASE_DIR, 'static', 'templates', 'certificado_venda')