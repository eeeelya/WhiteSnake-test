import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_shop.settings")

app = Celery("car_shop")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
