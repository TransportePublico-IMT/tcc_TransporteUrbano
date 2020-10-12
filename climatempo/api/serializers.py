from rest_framework.serializers import ModelSerializer

from climatempo.models import ClimaTempo


class ClimaTempoSerializer(ModelSerializer):
    class Meta:
        model = ClimaTempo
        fields = (
            "id_cidade",
            "temperatura",
            "direcao_vento",
            "velocidade_vento",
            "umidade",
            "condicao",
            "pressao",
            "sensacao",
            "date",
        )
