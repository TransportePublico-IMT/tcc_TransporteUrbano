from rest_framework.serializers import ModelSerializer
from onibus.models import Onibus

class OnibusSerializer(ModelSerializer):
    class Meta:
        model = Onibus
        fields = ('id', 'prefixo', 'cod_linha', 'lotacao', 'latitude', 'longitude')