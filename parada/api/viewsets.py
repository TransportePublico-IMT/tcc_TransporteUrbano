import time

from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from parada.models import Parada

from .serializers import ParadaSerializer


class ParadaViewSet(ModelViewSet):
    serializer_class = ParadaSerializer
    queryset = Parada.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            for i in request.data["p"]:
                Parada.objects.get_or_create(
                    id_parada=i["id_parada"],
                    nome=i["nome"],
                    endereco=i["endereco"],
                    latitude=i["latitude"],
                    longitude=i["longitude"],
                )
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})
