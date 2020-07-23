from django.db import models

class Onibus(models.Model):
    prefixo = models.IntegerField()
    cod_linha = models.IntegerField()
    lotacao = models.CharField(max_length=30)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.prefixo)