from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from onibus.models import Onibus
from .serializers import OnibusSerializer 
from helpers.processar_img import processar_img
import random

class OnibusViewSet(ModelViewSet):
    serializer_class = OnibusSerializer

    def get_queryset(self):
        lotacao = self.request.query_params.get('lotacao', None)
        queryset = Onibus.objects.all()
        if lotacao:
            queryset = Onibus.objects.filter(lotacao=lotacao)
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
            onibus = Onibus(
                prefixo = prefixo,
                cod_linha = cod_linha,
                lotacao = estado,
                latitude = latitude,
                longitude = longitude
            )
            onibus.save()
            return Response({'status': 'sucesso'})
        except:
            return Response({'status': 'erro'})
