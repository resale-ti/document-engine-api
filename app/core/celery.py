from celery import Celery
from core import celeryconfig

celery_app = Celery('document-engine-worker')

celery_app.config_from_object(celeryconfig)

celery_app.conf.task_routes = {
    'contract.generate_document': 'document-engine-queue'
}
