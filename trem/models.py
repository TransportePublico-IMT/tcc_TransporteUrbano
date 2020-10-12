from django.db import models


class Trem(models.Model):
    id_linha = models.IntegerField()
    data_ocorrencia = models.DateTimeField()
    descricao = models.CharField(max_length=1500, null=True)
    ultima_atualizacao = models.DateTimeField()
    situacao = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id_linha)
