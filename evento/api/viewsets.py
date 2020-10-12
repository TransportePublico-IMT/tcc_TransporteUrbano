from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import datetime
from evento.models import Evento
from .serializers import EventoSerializer

import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.ENV")
load_dotenv(dotenv_path)


class EventoViewSet(ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            for i in request.data["e"]:
                obj, created = Evento.objects.update_or_create(
                    link = i["link"],
                    defaults={
                        'nome': i["nome"],
                        'data_info': i["data_info"],
                        'data': i["data"],
                        'endereco': i["endereco"],
                        'latitude': i["latitude"],
                        'longitude': i["longitude"],
                    },
                )           
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})
    
    @action(methods=["GET"], detail=False)
    def proximos(self, request):
        if os.getenv("AMBIENTE").lower() == 'des':
            agora_utc = datetime.datetime.now() + datetime.timedelta(hours=3)
        elif os.getenv("AMBIENTE").lower() == 'prod':
            agora_utc = datetime.datetime.now()
        time_threshold = agora_utc
        eventos = Evento.objects.filter(
            data__gt=time_threshold
        )
        
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data)