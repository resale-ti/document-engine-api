from celery import Celery
from core import celeryconfig

celery_app = Celery('document-engine-worker')

celery_app.config_from_object(celeryconfig)

celery_app.conf.task_routes = {
    'regulamento_concorrencia.generate_document': 'document-engine-queue',
    'regulamento_concorrencia_completo.generate_document': 'document-engine-queue',
    'certificado_venda.generate_document': 'document-engine-queue',
    'edital.generate_document': 'document-engine-queue',
    
}
