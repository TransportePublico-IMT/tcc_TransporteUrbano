from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from climatempo.models import ClimaTempo

from .serializers import ClimaTempoSerializer


class ClimaTempoViewSet(ModelViewSet):
    serializer_class = ClimaTempoSerializer
    queryset = ClimaTempo.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            list_climatempo = []
            for i in request.data["ct"]:
                clima = ClimaTempo(
                    id_cidade=i["id_cidade"],
                    temperatura=i["temperatura"],
                    direcao_vento=i["direcao_vento"],
                    velocidade_vento=i["velocidade_vento"],
                    umidade=i["umidade"],
                    condicao=i["condicao"],
                    pressao=i["pressao"],
                    sensacao=i["sensacao"],
                )
                list_climatempo.append(clima)
            ClimaTempo.objects.bulk_create(list_climatempo)
            return Response({"status": "sucesso"})
        except Exception as e:
            return Response({"status": "erro: " + type(e).__name__ + ": " + str(e)})
