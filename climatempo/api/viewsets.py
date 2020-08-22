from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from climatempo.models import ClimaTempo
from .serializers import ClimaTempoSerializer
from rest_framework.decorators import action

class ClimaTempoViewSet(ModelViewSet):
    serializer_class = ClimaTempoSerializer
    queryset = ClimaTempo.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            list_climatempo = []
            for i in request.data['ct']:
                clima = ClimaTempo(
                    id_cidade =  i['id_cidade'],
                    temperatura = i['temperatura'],
                    direcao_vento = i['direcao_vento'],
                    velocidade_vento = i['velocidade_vento'],
                    umidade = i['umidade'],
                    condicao = i['condicao'],
                    pressao = i['pressao'],
                    sensacao = i['sensacao']
                    )
                list_climatempo.append(clima)
            ClimaTempo.objects.bulk_create(list_climatempo)
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})

    @action(methods=['GET'], detail=False)
    def ultimo(self, request):
        queryset = ClimaTempo.objects.order_by('-date').first()
        serializer = ClimaTempoSerializer(queryset)
        return Response(serializer.data)