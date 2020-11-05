import datetime
import random
import time
from datetime import timedelta
from itertools import chain

from django.db import connection
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from helpers.processar_img import processar_img
from linha.models import Linha
from onibus.models import (
    OnibusLotacao,
    OnibusPosicao,
    OnibusVelocidade,
    OnibusVelocidadeCoordenadas,
)

from .serializers import (
    OnibusLotacaoSerializer,
    OnibusPosicaoSerializer,
    OnibusVelocidadeSerializer,
)

import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../.ENV")
load_dotenv(dotenv_path)


class OnibusLotacaoViewSet(ModelViewSet):
    serializer_class = OnibusLotacaoSerializer

    def get_queryset(self):
        lotacao = self.request.query_params.get("lotacao", None)
        queryset = OnibusLotacao.objects.all()
        if lotacao:
            queryset = OnibusLotacao.objects.filter(lotacao=lotacao)
        return queryset

    def create(self, request, *args, **kwargs):
        try:
            img_path = request.data["img"]
            id_onibus = request.data["id_onibus"]
            id_linha = Linha.objects.get(id_linha=request.data["id_linha"])
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            # processar a imagem
            estado = processar_img(img_path)
            onibus_lotacao = OnibusLotacao(
                id_onibus=id_onibus,
                id_linha=id_linha,
                lotacao=estado,
                latitude=latitude,
                longitude=longitude,
            )
            onibus_lotacao.save()
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})

    @action(methods=["GET"], detail=False)
    def ultimos(self, request):
        intervalo = self.request.query_params.get("intervalo", None)
        lotacao = self.request.query_params.get("lotacao", None)
        query_add = ""
        if lotacao:
            query_add = f"AND lotacao = '{lotacao}'"
        if intervalo:
            queryset = OnibusLotacao.objects.raw(
                f"""SELECT *
                                                    FROM onibus_onibuslotacao
                                                    WHERE data_inclusao IN (
                                                        SELECT MAX(data_inclusao)
                                                        FROM onibus_onibuslotacao
                                                        WHERE data_inclusao >= DATETIME(DATETIME('now'), '-{intervalo} hours')
                                                        GROUP BY id_onibus
                                                    ){query_add};"""
            )

            serializer = OnibusLotacaoSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            queryset = OnibusLotacao.objects.raw(
                f"""SELECT *
                                                    FROM onibus_onibuslotacao
                                                    WHERE data_inclusao IN (
                                                        SELECT MAX(data_inclusao)
                                                        FROM onibus_onibuslotacao
                                                        GROUP BY id_onibus
                                                    ){query_add};"""
            )

            serializer = OnibusLotacaoSerializer(queryset, many=True)
            return Response(serializer.data)


class OnibusPosicaoViewSet(ModelViewSet):
    serializer_class = OnibusPosicaoSerializer
    queryset = OnibusPosicao.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            lista_onibus_posicao = []
            for i in request.data["o"]:
                onibus = OnibusPosicao(
                    id_onibus=i["id_onibus"],
                    onibus_deficiente=i["onibus_deficiente"],
                    horario_atualizacao_localizacao=i[
                        "horario_atualizacao_localizacao"
                    ],
                    latitude=i["latitude"],
                    longitude=i["longitude"],
                    frota=i["frota"],
                    id_linha=Linha.objects.get(id_linha=i["id_linha"]),
                )
                lista_onibus_posicao.append(onibus)
            OnibusPosicao.objects.bulk_create(lista_onibus_posicao)
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})

    @action(methods=["GET"], detail=False)
    def quantidade(self, request):
        try:
            data_inicial = self.request.query_params.get("data-inicial", None)
            data_final = self.request.query_params.get("data-final", None)

            if data_inicial is None or data_final is None:
                today = datetime.date.today()
                data_inicial = datetime.datetime.combine(
                    today, datetime.datetime.min.time()
                )
                data_final = datetime.datetime.combine(
                    today, datetime.datetime.max.time()
                )
            else:
                data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d %H:%M:%S")
                data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d %H:%M:%S")

            if os.getenv("AMBIENTE").lower() == 'des':
                data_inicial = str(data_inicial + datetime.timedelta(hours=3))
                data_final = str(data_final + datetime.timedelta(hours=3))
            elif os.getenv("AMBIENTE").lower() == 'prod':
                data_inicial = str(data_inicial)
                data_final = str(data_final)

            query = f"""SELECT COUNT(id_onibus) AS TOTAL
                        FROM (
                            SELECT id_onibus
                            FROM onibus_onibusposicao
                            WHERE data_inclusao IN (
                                SELECT MAX(data_inclusao)
                                FROM onibus_onibusposicao
                                WHERE data_inclusao BETWEEN '{data_inicial}' AND '{data_final}'
                                GROUP BY id_onibus
                            )
                            GROUP BY id_onibus
                        ) a;"""

            with connection.cursor() as cursor:
                cursor.execute(query)
                row = cursor.fetchone()

            return Response({"quantidade": row[0]})
        except Exception as e:
            return Response({"erro": type(e).__name__ + ": " + str(e)})


class OnibusVelocidadeViewSet(ModelViewSet):
    serializer_class = OnibusVelocidadeSerializer
    queryset = OnibusVelocidade.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            lista_onibus_velocidade = []
            todas_coordenadas = []

            for i in request.data["o"]:
                # cria objetos onibus_velocidade e adiciona em uma lista (não salva no db)
                onibus_velocidade = OnibusVelocidade(
                    nome=i["name"],
                    vel_trecho=i["description"]["vel_trecho"],
                    vel_via=i["description"]["vel_via"],
                    trecho=i["description"]["trecho"],
                    extensao=i["description"]["extensao"],
                    tempo=i["description"]["tempo"],
                )
                lista_onibus_velocidade.append(onibus_velocidade)
            OnibusVelocidade.objects.bulk_create(lista_onibus_velocidade)

            k = 0
            id_inicial = ""
            primeira_execucao = True
            if os.getenv("AMBIENTE").lower() == 'des':
                agora_utc = datetime.datetime.now() + timedelta(hours=3)
            elif os.getenv("AMBIENTE").lower() == 'prod':
                agora_utc = datetime.datetime.now()
            time_threshold = agora_utc - timedelta(minutes=1)
            onibus_velocidade = OnibusVelocidade.objects.filter(
                data_inclusao__gt=time_threshold  # pega valores maiores do que um minuto (que acabou de salvar) atrás, para nao filtrar o db todo
            )
            onibus_velocidade = list(onibus_velocidade)

            for i in request.data["o"]:
                # para saber qual é o certo, deve-se pegar o objeto cujo id bate com a iteração atual
                if primeira_execucao:
                    if len(onibus_velocidade) > 1:
                        id_iniciais = []
                        for x in onibus_velocidade:
                            id_iniciais.append(x.id)
                        id_inicial = min(id_iniciais)
                    else:
                        id_inicial = onibus_velocidade[0].id

                onibus_velocidade_certo = ""
                for x in onibus_velocidade:
                    if (
                        x.id == id_inicial + k
                    ):  # id_inicial + k é o objeto cujo id bate com a iteração atual
                        onibus_velocidade_certo = x

                lista_coordenadas = []
                for j in i["coordinates"]:
                    coordenadas = OnibusVelocidadeCoordenadas(
                        latitude=j["lat"],
                        longitude=j["lon"],
                        trecho=lista_onibus_velocidade[k].trecho,
                        onibus_velocidade=onibus_velocidade_certo,
                    )
                    lista_coordenadas.append(coordenadas)

                primeira_execucao = False
                k += 1
                todas_coordenadas.append(lista_coordenadas)

            # chain remove nested lists e transforma tudo em uma list só
            todas_coordenadas = list(chain.from_iterable(todas_coordenadas))

            OnibusVelocidadeCoordenadas.objects.all().delete()
            with connection.cursor() as cursor:
                if os.getenv("AMBIENTE").lower() == 'des':
                    cursor.execute("delete from onibus_onibusvelocidadecoordenadas;")
                    cursor.execute("delete from sqlite_sequence where name='onibus_onibusvelocidadecoordenadas';")
                if os.getenv("AMBIENTE").lower() == 'prod':
                    cursor.execute("ALTER SEQUENCE onibus_onibusvelocidadecoordenadas_id_seq RESTART WITH 1;")
            OnibusVelocidadeCoordenadas.objects.bulk_create(todas_coordenadas)
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})

    @action(methods=["GET"], detail=False)
    def ultimos(self, request):
        queryset = OnibusVelocidade.objects.raw(
            f"""SELECT *
                FROM onibus_onibusvelocidade
                WHERE data_inclusao IN (
                    SELECT MAX(data_inclusao)
                    FROM onibus_onibusvelocidade
                    GROUP BY trecho
                );"""
        )

        serializer = OnibusVelocidadeSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def historico(self, request):
        try:
            data_inicial = self.request.query_params.get("data-inicial", None)
            data_final = self.request.query_params.get("data-final", None)

            if data_inicial is None or data_final is None:
                today = (datetime.datetime.now() - datetime.timedelta(hours=3)).date()
                data_inicial = datetime.datetime.combine(today, datetime.datetime.min.time())
                data_final = datetime.datetime.combine(today, datetime.datetime.max.time())
            else:
                data_inicial = datetime.datetime.strptime(data_inicial, "%Y-%m-%d")
                data_inicial = datetime.datetime.combine(data_inicial, datetime.datetime.min.time())
                data_final = datetime.datetime.strptime(data_final, "%Y-%m-%d")
                data_final = datetime.datetime.combine(data_final, datetime.datetime.max.time())

            if os.getenv("AMBIENTE").lower() == 'des':
                data_inicial = str(data_inicial + datetime.timedelta(hours=6))
                data_final = str(data_final + datetime.timedelta(hours=6))
            elif os.getenv("AMBIENTE").lower() == 'prod':
                data_inicial = str(data_inicial + datetime.timedelta(hours=3))
                data_final = str(data_final + datetime.timedelta(hours=3))

            if os.getenv("AMBIENTE").lower() == 'des':
                query = f"""SELECT strftime('%H:%M', T1.INTERVALO) AS INTERVALO,
                            COALESCE(T2.VERDE, 0) AS VERDE,
                            COALESCE(T2.AMARELO, 0) AS AMARELO,
                            COALESCE(T2.VERMELHO, 0) AS VERMELHO,
                            COALESCE(T3.ONIBUS_CIRCULANDO, 0) AS ONIBUS_CIRCULANDO
                            FROM intervalo_intervalo T1
                            LEFT JOIN( 
                                select INTERVALO,
                                SUM(VERDE) AS VERDE,
                                SUM(AMARELO) AS AMARELO,
                                SUM(VERMELHO) AS VERMELHO
                                from(
                                    SELECT INTERVALO,
                                    CASE WHEN COR = 'AMARELO' THEN TRECHOS END AS AMARELO,
                                    CASE WHEN COR = 'VERDE' THEN TRECHOS END AS VERDE,
                                    CASE WHEN COR = 'VERMELHO' THEN TRECHOS END AS VERMELHO
                                    FROM (
                                        SELECT
                                        time((strftime('%H', HORARIO)) || ':' ||
                                        case when ((strftime('%M', HORARIO) / 30) * 30) = 0
                                        then '00'
                                        else '30' end) as INTERVALO,
                                        COR,
                                        CAST(AVG(QTD) as int) as TRECHOS
                                        from(
                                            SELECT strftime('%H:%M', data_inclusao) as HORARIO,
                                            case
                                            when vel_trecho >= (select avg(vel_trecho) FROM onibus_onibusvelocidade) then 'VERDE'
                                            when vel_trecho >= (select avg(vel_trecho) - 3 FROM onibus_onibusvelocidade) then 'AMARELO'
                                            else 'VERMELHO'
                                            end as COR,
                                            count(*) as QTD
                                            FROM onibus_onibusvelocidade
                                            WHERE data_inclusao between '{data_inicial}' and '{data_final}'
                                            GROUP BY strftime('%H%M', data_inclusao), COR
                                        ) a
                                        group by INTERVALO, COR
                                    ) b
                                )
                                group by INTERVALO
                                ) T2
                            ON T1.intervalo = T2.INTERVALO
                            LEFT JOIN
                                (SELECT
                                time((strftime('%H', HORARIO)) || ':' ||
                                case when ((strftime('%M', HORARIO) / 30) * 30) = 0
                                then '00'
                                else '30' end) as INTERVALO,
                                CAST(AVG(QTD) as int) as ONIBUS_CIRCULANDO
                                from(
                                    SELECT strftime('%H:%M', data_inclusao) as HORARIO,
                                    count(*) as QTD
                                    FROM onibus_onibusposicao
                                    WHERE data_inclusao between '{data_inicial}' and '{data_final}'
                                    GROUP BY strftime('%H%M', data_inclusao)
                                ) a
                                group by INTERVALO) T3
                            ON(T1.INTERVALO = T3.INTERVALO);"""

            elif os.getenv("AMBIENTE").lower() == 'prod':
                query = f"""SELECT to_char(T1.INTERVALO, 'HH24:MI') AS INTERVALO,
                        COALESCE(T2.VERDE, 0) AS VERDE,
                        COALESCE(T2.AMARELO, 0) AS AMARELO,
                        COALESCE(T2.VERMELHO, 0) AS VERMELHO,
                        COALESCE(T3.ONIBUS_CIRCULANDO, 0) AS ONIBUS_CIRCULANDO
                        FROM intervalo_intervalo T1
                        LEFT JOIN( 
                            select INTERVALO,
                            SUM(VERDE) AS VERDE,
                            SUM(AMARELO) AS AMARELO,
                            SUM(VERMELHO) AS VERMELHO
                            from(
                                SELECT INTERVALO,
                                CASE WHEN COR = 'AMARELO' THEN TRECHOS END AS AMARELO,
                                CASE WHEN COR = 'VERDE' THEN TRECHOS END AS VERDE,
                                CASE WHEN COR = 'VERMELHO' THEN TRECHOS END AS VERMELHO
                                FROM (
                                    SELECT
                                    TO_TIMESTAMP((to_char(HORARIO, 'HH24')) || ':' ||
                                    case when ((CAST(to_char(HORARIO, 'MI') AS INT) / 30) * 30) = 0
                                    then '00'
                                    else '30' end, 'HH24:MI')::TIME as INTERVALO,
                                    COR,
                                    CAST(AVG(QTD) as int) as TRECHOS
                                    from(
                                        SELECT TO_TIMESTAMP(to_char(data_inclusao, 'HH24:MI'), 'HH24:MI')::TIME as HORARIO,
                                        case
                                        when vel_trecho >= (select avg(vel_trecho) FROM onibus_onibusvelocidade) then 'VERDE'
                                        when vel_trecho >= (select avg(vel_trecho) - 3 FROM onibus_onibusvelocidade) then 'AMARELO'
                                        else 'VERMELHO'
                                        end as COR,
                                        count(*) as QTD
                                        FROM onibus_onibusvelocidade
                                        WHERE data_inclusao between '{data_inicial}' and '{data_final}'
                                        GROUP BY HORARIO, COR
                                    ) a
                                    group by INTERVALO, COR
                                ) b
                            ) c
                            group by INTERVALO
                            ) T2
                        ON T1.intervalo = T2.INTERVALO
                        LEFT JOIN
                            (SELECT
                            TO_TIMESTAMP((to_char(HORARIO, 'HH24')) || ':' ||
                            case when ((CAST(to_char(HORARIO, 'MI') AS INT) / 30) * 30) = 0
                            then '00'
                            else '30' end, 'HH24:MI')::TIME as INTERVALO,
                            CAST(AVG(QTD) as int) as ONIBUS_CIRCULANDO
                            from(
                                SELECT TO_TIMESTAMP(to_char(data_inclusao, 'HH24:MI'), 'HH24:MI')::TIME as HORARIO,
                                count(*) as QTD
                                FROM onibus_onibusposicao
                                WHERE data_inclusao between '{data_inicial}' and '{data_final}'
                                GROUP BY HORARIO
                            ) a
                            group by INTERVALO) T3
                        ON(T1.INTERVALO = T3.INTERVALO);"""

            with connection.cursor() as cursor:
                cursor.execute(query)
                retorno = cursor.fetchall()
                intervalo = []
                verde = []
                amarelo = []
                vermelho = []
                onibus_circulando = []
                for i in retorno:
                    intervalo.append(i[0])
                    verde.append(i[1])
                    amarelo.append(i[2])
                    vermelho.append(i[3])
                    onibus_circulando.append(i[4])
                dict_retorno = {
                    "data-inicial": data_inicial,
                    "data-final": data_final,
                    "intervalo": intervalo,
                    "verde": verde,
                    "amarelo": amarelo,
                    "vermelho": vermelho,
                    "onibus_circulando": onibus_circulando
                }

            return Response(dict_retorno)
        except Exception as e:
            return Response({"erro": type(e).__name__ + ": " + str(e)})