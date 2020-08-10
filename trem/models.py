from django.db import models

class Trem(models.Model):
    id_linha = models.IntegerField()
    data_ocorrencia = models.DateTimeField()
    descricao = models.CharField(max_length=1500, null=True)
    ultima_atualizacao = models.DateTimeField()
    situacao = models.CharField(max_length=300)

    def __str__(self):
        return str(self.id_linha)

# class ClimaTempo(models.Model):
#     id_cidade = models.IntegerField()
#     temperatura = models.DecimalField(max_digits=5, decimal_places=2)
#     direcao_vento = models.CharField(max_length=10)
#     velocidade_vento = models.DecimalField(max_digits=5, decimal_places=2)
#     umidade = models.DecimalField(max_digits=5, decimal_places=2)
#     condicao = models.CharField(max_length=500)
#     pressao = models.DecimalField(max_digits=10, decimal_places=2)
#     #icone = models.CharField(max_length=500)
#     sensacao = models.DecimalField(max_digits=5, decimal_places=2)
#     date = models.DateTimeField()

#     def __str__(self):
#         return str(self.temperatura)
