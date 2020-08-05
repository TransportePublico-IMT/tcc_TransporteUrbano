from rest_framework.serializers import ModelSerializer
from linha.models import Linha

class LinhaSerializer(ModelSerializer):
    class Meta:
        model = Linha
        fields = ('id_linha', 'letreiro', 'sentido', 'letreiro_destino', 'letreiro_origem')