from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from onibus.models import OnibusLotacao, OnibusPosicao, OnibusVelocidade, OnibusVelocidadeCoordenadas
from linha.models import Linha
from .serializers import OnibusLotacaoSerializer, OnibusPosicaoSerializer, OnibusVelocidadeSerializer
from helpers.processar_img import processar_img
from django.db import connection
import random
import datetime
from itertools import chain
from datetime import timedelta

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

    @action(methods=['GET'], detail=False)
    def quantidade(self, request):
        try:
            data_inicial = self.request.query_params.get('data-inicial', None)
            data_final = self.request.query_params.get('data-final', None)

            if data_inicial == None or data_final == None:
                today = datetime.date.today()
                data_inicial = datetime.datetime.combine(today, datetime.datetime.min.time())
                data_final = datetime.datetime.combine(today, datetime.datetime.max.time())
            else:
                data_inicial = datetime.datetime.strptime(data_inicial, '%Y-%m-%d %H:%M:%S')
                data_final = datetime.datetime.strptime(data_final, '%Y-%m-%d %H:%M:%S')

            data_inicial = str(data_inicial + datetime.timedelta(hours=3))
            data_final = str(data_final + datetime.timedelta(hours=3))

            query = f'''SELECT COUNT(*) AS TOTAL
                        FROM (
                            SELECT *
                            FROM onibus_onibusposicao
                            WHERE data_inclusao IN (
                                SELECT MAX(data_inclusao)
                                FROM onibus_onibusposicao
                                WHERE data_inclusao BETWEEN '{data_inicial}' AND '{data_final}'
                                GROUP BY id_onibus
                            )
                            GROUP BY id_onibus
                        );'''

            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()

            return Response({'quantidade': row[0]})
        except Exception as e:
            return Response({'erro': type(e).__name__ + ": " + str(e)})

class OnibusVelocidadeViewSet(ModelViewSet):
    serializer_class = OnibusVelocidadeSerializer
    queryset = OnibusVelocidade.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            lista_onibus_velocidade = []
            todas_coordenadas = []
            banco_populado = OnibusVelocidadeCoordenadas.objects.all().exists()
            
            for i in request.data['o']:

                #cria objetos onibus_velocidade e adiciona em uma lista (não salva no db)
                onibus_velocidade = OnibusVelocidade(
                    nome = i['name'],
                    vel_trecho = i['description']['vel_trecho'],
                    vel_via = i['description']['vel_via'],
                    trecho = i['description']['trecho'],
                    extensao = i['description']['extensao'],
                    tempo = i['description']['tempo']
                )
                lista_onibus_velocidade.append(onibus_velocidade)
            OnibusVelocidade.objects.bulk_create(lista_onibus_velocidade)

            k=0
            id_inicial = ''
            primeira_execucao = True
            agora_utc = datetime.datetime.now() + timedelta(hours=3)
            time_threshold = agora_utc - timedelta(minutes=2)
            for i in request.data['o']:
                onibus_velocidade = OnibusVelocidade.objects.filter(
                        nome = lista_onibus_velocidade[k].nome,
                        vel_trecho = lista_onibus_velocidade[k].vel_trecho,
                        vel_via = lista_onibus_velocidade[k].vel_via,
                        trecho = lista_onibus_velocidade[k].trecho,
                        extensao = lista_onibus_velocidade[k].extensao,
                        tempo = lista_onibus_velocidade[k].tempo,
                        data_inclusao__gt=time_threshold #pega valores maiores do que dois minutos atrás, para nao filtrar o db todo
                    )
                onibus_velocidade = list(onibus_velocidade)

                #esse processamento se deve ao fato de as vezes o onibus_velocidade retornar 2 objetos
                #para saber qual é o certo, deve-se pegar o objeto da iteração que estamos
                if primeira_execucao:
                    if len(onibus_velocidade) > 1:
                        id_iniciais = []
                        for x in onibus_velocidade:
                            id_iniciais.append(x.id)
                        id_inicial = min(id_iniciais)
                    else:
                        id_inicial = onibus_velocidade[0].id
                
                onibus_velocidade_certo = ''
                for x in onibus_velocidade:
                    if x.id == id_inicial + k:
                        onibus_velocidade_certo = x
                
                primeira_execucao = False
                lista_coordenadas = []
                for j in i['coordinates']:
                    coordenadas = OnibusVelocidadeCoordenadas(
                        latitude = j['lat'],
                        longitude = j['lon'],
                        trecho = lista_onibus_velocidade[k].trecho,
                        onibus_velocidade = onibus_velocidade_certo
                    )
                    lista_coordenadas.append(coordenadas)
                k+=1
                todas_coordenadas.append(lista_coordenadas)
                            
            #chain remove nested lists e transforma tudo em uma list só
            todas_coordenadas = list(chain.from_iterable(todas_coordenadas))
            coordenadas_update = []
            if banco_populado:
                for i in todas_coordenadas:
                    coordenadas = OnibusVelocidadeCoordenadas.objects.filter(
                            latitude = i.latitude,
                            longitude = i.longitude,
                            trecho = i.trecho
                        )
                    #esse for existe para caso retorne duas coordenadas (no caso de ser null irá retornar)
                    for j in list(coordenadas):
                        j.onibus_velocidade = i.onibus_velocidade
                        coordenadas_update.append(j)
                    
                OnibusVelocidadeCoordenadas.objects.bulk_update(coordenadas_update, ['onibus_velocidade'])
            else:
                OnibusVelocidadeCoordenadas.objects.bulk_create(todas_coordenadas)
                
            return Response({'status': 'sucesso'})
        except Exception as e:
            return Response({'status': 'erro: ' + type(e).__name__ + ": " + str(e)})
    
    @action(methods=['GET'], detail=False)
    def ultimos(self, request):
        # queryset = OnibusLotacao.objects.order_by('-data_inclusao').distinct('id_onibus')
        queryset = OnibusVelocidade.objects.raw(f'''SELECT *
                                                FROM onibus_onibusvelocidade
                                                WHERE data_inclusao IN (
                                                    SELECT MAX(data_inclusao)
                                                    FROM onibus_onibusvelocidade
                                                    GROUP BY trecho
                                                );''')

        serializer = OnibusVelocidadeSerializer(queryset, many=True)
        return Response(serializer.data)