from rest_framework.serializers import ModelSerializer

from evento.models import Evento


class EventoSerializer(ModelSerializer):
    class Meta:
        model = Evento
        fields = "__all__"