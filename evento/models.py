from django.db import models

class Evento(models.Model):
    nome = models.CharField(max_length=255)
    link = models.CharField(max_length=500)
    data_info = models.CharField(max_length=500, null=True)
    data = models.DateField(null=True)
    endereco = models.CharField(max_length=700, null=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=15, null=True)
    longitude = models.DecimalField(max_digits=17, decimal_places=15, null=True)
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nome)
