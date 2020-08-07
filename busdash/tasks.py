from celery.task.schedules import crontab
from celery.decorators import periodic_task
from helpers import popular_db_sp_trans
from helpers import popular_db_apis
import time

#celery -A busdash worker --pool=eventlet -l info

class TaskFailure(Exception):
   pass

@periodic_task(run_every=(crontab(minute='*/30')), name="create_paradas_if_not_exist", ignore_result=True)
def create_paradas_if_not_exist():
    status_json = popular_db_sp_trans.popular_paradas()
    status = status_json['status']
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status

@periodic_task(run_every=(crontab(minute='*/1')), name="create_linhas_if_not_exist", ignore_result=True)
def create_linhas_if_not_exist():
    status_json = popular_db_sp_trans.popular_linhas()
    status = status_json['status']
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status

@periodic_task(run_every=(crontab(minute='*/5')), name="save_onibus_posicao", ignore_result=True)
def save_onibus_posicao():
    status_json = popular_db_sp_trans.popular_onibus()
    status = status_json['status']
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status

@periodic_task(run_every=(crontab(minute='*/1')), name="save_trens_metros", ignore_result=True)
def save_trens_metros():
    status_json = popular_db_apis.popular_trens_metros()
    status = status_json['status']
    if status.startswith("erro"):
        raise TaskFailure(status)
    return status