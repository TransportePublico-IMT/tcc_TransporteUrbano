from django.db import models
from linha.models import Linha

class OnibusLotacao(models.Model):
    id_onibus = models.IntegerField()
    id_linha = models.ForeignKey(Linha, to_field="id_linha", db_column="id_linha", on_delete=models.SET_NULL, null=True)
    lotacao = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_onibus)

class OnibusPosicao(models.Model):
    id_onibus = models.IntegerField()
    onibus_deficiente = models.BooleanField()
    data_inclusao = models.DateTimeField(auto_now_add=True)
    horario_atualizacao_localizacao = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    id_linha = models.ForeignKey(Linha, to_field="id_linha", db_column="id_linha", on_delete=models.SET_NULL, null=True)
    frota = models.IntegerField()

    def __str__(self):
        return str(self.id_onibus)