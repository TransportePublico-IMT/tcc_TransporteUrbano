from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from evento.models import Evento

from .serializers import EventoSerializer


class EventoViewSet(ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            list_eventos = []
            for i in request.data["e"]:
                evento = Evento(
                    nome = i["nome"],
                    link = i["link"],
                    data = i["data"],
                    endereco = i["endereco"],
                    latitude = i["latitude"],
                    longitude = i["longitude"]
                )
                list_eventos.append(evento)
            Evento.objects.bulk_create(list_eventos)
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})