from rest_framework.serializers import ModelSerializer

from parada.models import Parada


class ParadaSerializer(ModelSerializer):
    class Meta:
        model = Parada
        fields = ("id", "id_parada", "nome", "endereco", "latitude", "longitude")
