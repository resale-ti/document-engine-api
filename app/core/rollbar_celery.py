from utils.rollbar import rollbar as rollbar_celery


def celery_base_data_hook(request, data):
    data['framework'] = 'celery'


rollbar_celery.BASE_DATA_HOOK = celery_base_data_hook
