from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from onibus.models import OnibusLotacao, OnibusPosicao
from linha.models import Linha
from .serializers import OnibusLotacaoSerializer, OnibusPosicaoSerializer
from helpers.processar_img import processar_img
import random

class OnibusLotacaoViewSet(ModelViewSet):
    serializer_class = OnibusLotacaoSerializer

    def get_queryset(self):
        lotacao = self.request.query_params.get('lotacao', None)
        queryset = OnibusLotacao.objects.all()
        if lotacao:
            queryset = OnibusLotacao.objects.filter(lotacao=lotacao)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            img_path = request.data['img']
            id_onibus = request.data['id_onibus']
            id_linha = Linha.objects.get(id_linha=request.data['id_linha'])
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            #processar a imagem
            estado = processar_img(img_path)
            onibus_lotacao = OnibusLotacao(
                id_onibus = id_onibus,
                id_linha = id_linha,
                lotacao = estado,
                latitude = latitude,
                longitude = longitude
            )
            onibus_lotacao.save()
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})

    @action(methods=['GET'], detail=False)
    def ultimos(self, request):
        intervalo = self.request.query_params.get('intervalo', None)
        lotacao = self.request.query_params.get('lotacao', None)
        query_add = ""
        if lotacao:
            query_add = f"AND lotacao = '{lotacao}'"
        if intervalo:
            queryset = OnibusLotacao.objects.raw(f'''SELECT *
                                                    FROM onibus_onibuslotacao
                                                    WHERE data_inclusao IN (
                                                        SELECT MAX(data_inclusao)
                                                        FROM onibus_onibuslotacao
                                                        WHERE data_inclusao >= DATETIME(DATETIME('now'), '-{intervalo} hours')
                                                        GROUP BY id_onibus
                                                    ){query_add};''')
            
            serializer = OnibusLotacaoSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # queryset = OnibusLotacao.objects.order_by('-data_inclusao').distinct('id_onibus')
            queryset = OnibusLotacao.objects.raw(f'''SELECT *
                                                    FROM onibus_onibuslotacao
                                                    WHERE data_inclusao IN (
                                                        SELECT MAX(data_inclusao)
                                                        FROM onibus_onibuslotacao
                                                        GROUP BY id_onibus
                                                    ){query_add};''')

            serializer = OnibusLotacaoSerializer(queryset, many=True)
            return Response(serializer.data)

        


class OnibusPosicaoViewSet(ModelViewSet):
    serializer_class = OnibusPosicaoSerializer
    queryset = OnibusPosicao.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            lista_onibus_posicao = []
            for i in request.data['o']:
                onibus = OnibusPosicao(
                    id_onibus =  i['id_onibus'],
                    onibus_deficiente = i["onibus_deficiente"],
                    horario_atualizacao_localizacao = i["horario_atualizacao_localizacao"],
                    latitude = i["latitude"],
                    longitude = i["longitude"],
                    frota = i["frota"],
                    id_linha = Linha.objects.get(id_linha=i["id_linha"])
                )
                lista_onibus_posicao.append(onibus)
            OnibusPosicao.objects.bulk_create(lista_onibus_posicao)
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})