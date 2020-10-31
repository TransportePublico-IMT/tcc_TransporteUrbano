from django.db import models

class Intervalo(models.Model):
    intervalo = models.TimeField()

    def __str__(self):
        return str(self.intervalo)