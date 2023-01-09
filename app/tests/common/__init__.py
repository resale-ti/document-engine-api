from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PATH_CONTRACTS = os.path.join(BASE_DIR, 'api', 'contract')