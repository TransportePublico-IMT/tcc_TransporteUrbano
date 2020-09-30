import time
from datetime import datetime

from celery import shared_task
from celery.decorators import periodic_task
from celery.task.schedules import crontab

from helpers import popular_db_apis, popular_db_sp_trans, processar_kmz

# celery -A busdash worker --pool=eventlet -l info --detach

# celery -A busdash beat -l info --detach


class TaskFailure(Exception):
    pass


@periodic_task(
    run_every=(crontab(minute="*/30")),
    name="create_paradas_if_not_exist",
    ignore_result=True,
)
def create_paradas_if_not_exist():
    status_json = popular_db_sp_trans.popular_paradas()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status


@periodic_task(
    run_every=(crontab(minute="*/1")),
    name="create_linhas_if_not_exist",
    ignore_result=True,
)
def create_linhas_if_not_exist():
    status_json = popular_db_sp_trans.popular_linhas()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status


@periodic_task(
    run_every=(crontab(minute="*/5")), name="save_onibus_posicao", ignore_result=True
)
def save_onibus_posicao():
    status_json = popular_db_sp_trans.popular_onibus()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status


@periodic_task(
    run_every=(crontab(minute="*/10")), name="save_trens_metros", ignore_result=True
)
def save_trens_metros():
    status_json = popular_db_apis.popular_trens_metros()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status


@periodic_task(
    run_every=(crontab(minute="*/5")), name="save_clima_tempo", ignore_result=True
)
def save_clima_tempo():
    status_json = popular_db_apis.popular_climatempo()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status


@periodic_task(
    run_every=(crontab(minute="*/15")),
    name="save_onibus_velocidade",
    ignore_result=True,
)
def save_onibus_velocidade():
    status_json = processar_kmz.popular_onibus_velocidade()
    status = status_json["status"]
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status
