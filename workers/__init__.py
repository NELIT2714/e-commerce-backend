import os

from celery import Celery

celery = Celery(
    "tasks",
    broker="redis://celery:E!ggCkc7BYgxmUKN@iBf@Q!voVsDm_!8@maximum.style:6379/10",
    backend="redis://celery:E!ggCkc7BYgxmUKN@iBf@Q!voVsDm_!8@maximum.style:6379/10",
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Europe/Warsaw",
    enable_utc=True,
    broker_transport_options={
        "global_keyprefix": "celery.broker.",
        "fanout_prefix": "/celery{db}.",
    },
    result_backend_transport_options={
        "global_keyprefix": "celery.broker.",
    },
    task_routes={
        "workers.save_files": {"queue": "files"},
    }
)

celery.autodiscover_tasks(["workers"])
