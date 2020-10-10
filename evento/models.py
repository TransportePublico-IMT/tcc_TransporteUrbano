from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=255)
    link = models.CharField(max_length=500)
    data = models.CharField(max_length=500)
    endereco = models.CharField(max_length=700)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nome)
