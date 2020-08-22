from django.db import models

class ClimaTempo(models.Model):
    id_cidade = models.IntegerField()
    temperatura = models.DecimalField(max_digits=5, decimal_places=2)
    direcao_vento = models.CharField(max_length=10)
    velocidade_vento = models.DecimalField(max_digits=5, decimal_places=2)
    umidade = models.DecimalField(max_digits=5, decimal_places=2)
    condicao = models.CharField(max_length=500, null=True)
    pressao = models.DecimalField(max_digits=10, decimal_places=2)
    sensacao = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.temperatura)
