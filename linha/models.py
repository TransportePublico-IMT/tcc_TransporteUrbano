from django.db import models


class Linha(models.Model):
    id_linha = models.IntegerField(unique=True)
    letreiro = models.CharField(max_length=80)
    sentido = models.IntegerField()
    letreiro_destino = models.CharField(max_length=80)
    letreiro_origem = models.CharField(max_length=80)

    def __str__(self):
        return str(self.letreiro)
