from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from trem.models import Trem
from .serializers import TremSerializer

class TremViewSet(ModelViewSet):
    serializer_class = TremSerializer
    queryset = Trem.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            list_trem = []
            for i in request.data['t']:
                trem = Trem(
                    id_linha =  i['id_linha'],
                    data_ocorrencia = i["data_ocorrencia"],
                    descricao = i["descricao"],
                    ultima_atualizacao = i["ultima_atualizacao"],
                    situacao = i["situacao"]
                    )
                list_trem.append(trem)
            Trem.objects.bulk_create(list_trem)
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})


#     def create(self, request, *args, **kwargs):
#         try:
#             list_climatempo = []
#             for i in request.data['ct']:
#                 clima = ClimaTempo(
#                     id_cidade =  i['id_cidade'],
#                     temperatura = i['temperatura'],
#                     direcao_vento = i['direcao_vento'],
#                     velocidade_vento = i['velocidade_vento'],
#                     umidade = i['umidade'],
#                     condicao = i['condicao'],
#                     pressao = i['pressao'],
#                     #icone = i['icone'],
#                     sensacao = i['sensacao'],
#                     date = i['date']
#                     )
#                 list_climatempo.append(clima)
#             ClimaTempo.objects.bulk_create(list_climatempo)
#             return Response({'status': 'sucesso'})
#         except Exception as e:
#             return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})
