from rest_framework.serializers import ModelSerializer

from onibus.models import OnibusLotacao


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
        model = OnibusLotacao
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
