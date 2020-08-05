from celery import shared_task
from helpers import popular_db_sp_trans
import time

@shared_task(bind=True)
def create_paradas_if_not_exist(self):
    status_json = popular_db_sp_trans.popular_paradas()
    return status_json['status']

@shared_task(bind=True)
def create_linhas_if_not_exist(self):
    status_json = popular_db_sp_trans.popular_linhas()
    return status_json['status']

@shared_task(bind=True)
def create_onibus(self):
    status_json = popular_db_sp_trans.popular_onibus()
    return status_json['status']