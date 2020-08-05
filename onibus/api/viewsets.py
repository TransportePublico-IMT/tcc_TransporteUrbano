from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from onibus.models import OnibusLotacao, OnibusPosicao
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
            prefixo = request.data['prefixo']
            cod_linha = request.data['cod_linha']
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            #processar a imagem
            estado = processar_img(img_path)
            onibus_lotacao = OnibusLotacao(
                prefixo = prefixo,
                cod_linha = cod_linha,
                lotacao = estado,
                latitude = latitude,
                longitude = longitude
            )
            onibus_lotacao.save()
            return Response({'status': 'sucesso'})
        except:
            return Response({'status': 'erro'})

class OnibusPosicaoViewSet(ModelViewSet):
    serializer_class = OnibusPosicaoSerializer
    queryset = OnibusPosicao.objects.all()