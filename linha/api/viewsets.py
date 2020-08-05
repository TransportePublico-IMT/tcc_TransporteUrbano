from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from linha.models import Linha
from .serializers import LinhaSerializer

class LinhaViewSet(ModelViewSet):
    serializer_class = LinhaSerializer
    queryset = Linha.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            for i in request.data['l']:
                Linha.objects.get_or_create(
                    id_linha =  i['id_linha'],
                    letreiro = i["letreiro"],
                    sentido = i["sentido"],
                    letreiro_destino = i["letreiro_destino"],
                    letreiro_origem = i["letreiro_origem"]
                )
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + str(e)})