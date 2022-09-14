from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import os
from api.routers import document, task_control, developer
from rollbar.contrib.fastapi import ReporterMiddleware as RollbarMiddleware

from rollbar.contrib.fastapi import LoggerMiddleware

import utils.rollbar

from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

if os.path.isfile(os.path.join(BASE_DIR, '.env')):
    load_dotenv()

app = FastAPI()

origins = os.environ.get('CORS_ORIGINS_AllOWED').split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RollbarMiddleware)
app.add_middleware(LoggerMiddleware)

@app.get("/", tags=['HealthCheck'], status_code=status.HTTP_200_OK)
async def health_check():
    return {'status': 'alive'}

app.include_router(task_control.router, prefix='/tasks', tags=['Tasks'])
app.include_router(document.router, prefix='/documents', tags=['Documents'])

# Router somente para desenvolvimento local, por aqui usamos somente FAST-API - conseguimos debugar.
if os.environ.get("STAGE") not in ["DEV", "PROD"]:
    app.include_router(developer.router, prefix='/local', tags=['Developer'])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost",
                port=8004, debug=True, reload=True)