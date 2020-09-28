from django.db import models

from linha.models import Linha


class OnibusLotacao(models.Model):
    id_onibus = models.IntegerField()
    id_linha = models.ForeignKey(
        Linha,
        to_field="id_linha",
        db_column="id_linha",
        on_delete=models.SET_NULL,
        null=True,
    )
    lotacao = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_onibus)


class OnibusPosicao(models.Model):
    id_onibus = models.IntegerField()
    onibus_deficiente = models.BooleanField()
    data_inclusao = models.DateTimeField(auto_now_add=True)
    horario_atualizacao_localizacao = models.DateTimeField()
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=17, decimal_places=15)
    id_linha = models.ForeignKey(
        Linha,
        to_field="id_linha",
        db_column="id_linha",
        on_delete=models.SET_NULL,
        null=True,
    )
    frota = models.IntegerField()

    def __str__(self):
        return str(self.id_onibus)


class OnibusVelocidade(models.Model):
    nome = models.CharField(max_length=300, null=True)
    vel_trecho = models.IntegerField(null=True)
    vel_via = models.IntegerField(null=True)
    trecho = models.CharField(max_length=300, null=True)
    extensao = models.IntegerField(null=True)
    tempo = models.CharField(max_length=5, null=True)
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.nome)


class OnibusVelocidadeCoordenadas(models.Model):
    trecho = models.CharField(max_length=300, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    onibus_velocidade = models.ForeignKey(
        OnibusVelocidade,
        related_name="coordenadas",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __eq__(self, other):
        return (
            self.latitude == other.latitude
            and self.longitude == other.longitude
            and self.trecho == other.trecho
        )

    def __lt__(self, other):
        return (
            float(self.latitude or 0) < float(other.latitude or 0)
            and float(self.longitude or 0) < float(other.longitude or 0)
            and self.trecho < other.trecho
        )

    def __gt__(self, other):
        return (
            float(self.latitude or 0) > float(other.latitude or 0)
            and float(self.longitude or 0) > float(other.longitude or 0)
            and self.trecho > other.trecho
        )

    def __hash__(self):
        return hash(("latitude", self.latitude, "longitude", self.longitude))

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.trecho}"
