from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from linha.models import Linha

from .serializers import LinhaSerializer


class LinhaViewSet(ModelViewSet):
    serializer_class = LinhaSerializer
    queryset = Linha.objects.all()

    def create(self, request, *args, **kwargs):
        i = ""
        try:
            for i in request.data["l"]:
                Linha.objects.get_or_create(
                    id_linha=i["id_linha"],
                    letreiro=i["letreiro"],
                    sentido=i["sentido"],
                    letreiro_destino=i["letreiro_destino"],
                    letreiro_origem=i["letreiro_origem"],
                )
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response(
                {
                    "status": f"erro: {type(e).__name__}: {str(e)} --- Esta tendo inserir: {i}"
                }
            )