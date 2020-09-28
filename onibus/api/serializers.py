from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from onibus.models import (
    OnibusLotacao,
    OnibusPosicao,
    OnibusVelocidade,
    OnibusVelocidadeCoordenadas,
)


class OnibusLotacaoSerializer(ModelSerializer):
    class Meta:
        model = OnibusLotacao
        fields = (
            "id",
            "id_onibus",
            "id_linha",
            "lotacao",
            "latitude",
            "longitude",
            "data_inclusao",
        )


class OnibusPosicaoSerializer(ModelSerializer):
    class Meta:
        model = OnibusPosicao
        fields = (
            "id",
            "id_onibus",
            "onibus_deficiente",
            "data_inclusao",
            "horario_atualizacao_localizacao",
            "latitude",
            "longitude",
            "id_linha",
            "frota",
        )


class OnibusVelocidadeCoordenadasSerializer(ModelSerializer):
    class Meta:
        model = OnibusVelocidadeCoordenadas
        fields = ("latitude", "longitude")


class OnibusVelocidadeSerializer(ModelSerializer):
    coordenadas = OnibusVelocidadeCoordenadasSerializer(many=True, read_only=True)

    class Meta:
        model = OnibusVelocidade
        fields = (
            "id",
            "nome",
            "vel_trecho",
            "vel_via",
            "trecho",
            "extensao",
            "tempo",
            "coordenadas",
        )
