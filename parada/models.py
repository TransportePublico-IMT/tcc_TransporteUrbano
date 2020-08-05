from django.db import models

class Parada(models.Model):
    id_parada = models.IntegerField()
    nome = models.CharField(max_length=80, blank=True)
    endereco = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)

    def __str__(self):
        return str(self.nome)