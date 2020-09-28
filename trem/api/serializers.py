from rest_framework.serializers import ModelSerializer

from trem.models import Trem


class TremSerializer(ModelSerializer):
    class Meta:
        model = Trem
        fields = (
            "id",
            "id_linha",
            "data_ocorrencia",
            "descricao",
            "ultima_atualizacao",
            "stiaucao",
        )
