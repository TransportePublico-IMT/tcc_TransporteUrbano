from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from trem.models import Trem

from .serializers import TremSerializer


class TremViewSet(ModelViewSet):
    serializer_class = TremSerializer
    queryset = Trem.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            list_trem = []
            for i in request.data["t"]:
                trem = Trem(
                    id_linha=i["id_linha"],
                    data_ocorrencia=i["data_ocorrencia"],
                    descricao=i["descricao"],
                    ultima_atualizacao=i["ultima_atualizacao"],
                    situacao=i["situacao"],
                )
                list_trem.append(trem)
            Trem.objects.bulk_create(list_trem)
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})

    @action(methods=["GET"], detail=False)
    def ultimos(self, request):
        # queryset = OnibusLotacao.objects.order_by('-data_inclusao').distinct('id_onibus')
        queryset = Trem.objects.raw(
            f"""SELECT *
                                        FROM trem_trem
                                        WHERE ultima_atualizacao IN (
                                            SELECT MAX(ultima_atualizacao)
                                            FROM trem_trem
                                            GROUP BY id_linha
                                        );"""
        )
        serializer = TremSerializer(queryset, many=True)
        return Response(serializer.data)
