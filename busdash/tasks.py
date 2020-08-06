from celery.task.schedules import crontab
from celery.decorators import periodic_task
from helpers import popular_db_sp_trans
import time

#celery -A busdash worker --pool=gevent -l info

@periodic_task(run_every=(crontab(minute='*/1')), name="create_paradas_if_not_exist", ignore_result=True)
def create_paradas_if_not_exist():
    status_json = popular_db_sp_trans.popular_paradas()
    return status_json['status']

@periodic_task(run_every=(crontab(minute='*/1')), name="create_linhas_if_not_exist", ignore_result=True)
def create_linhas_if_not_exist():
    status_json = popular_db_sp_trans.popular_linhas()
    return status_json['status']

@periodic_task(run_every=(crontab(minute='*/1')), name="save_onibus_posicao", ignore_result=True)
def save_onibus_posicao():
    status_json = popular_db_sp_trans.popular_onibus()
    return status_json['status']