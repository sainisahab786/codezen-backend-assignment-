import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_platform.settings')

app = Celery('ecommerce_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'import-products-daily': {
        'task': 'celery_tasks.tasks.import_products_task',
        'schedule': crontab(hour=14, minute=30),
        'args': ('/path/to/your/excel/file.xlsx',),
    },
}