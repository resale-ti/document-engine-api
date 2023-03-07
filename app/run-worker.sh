celery -A api.tasks worker -l info -Q document-engine-queue -c 1 --without-mingle -n workerDocument.%h
