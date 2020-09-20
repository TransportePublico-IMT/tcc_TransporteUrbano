from django.contrib import admin
from .models import OnibusLotacao, OnibusPosicao, OnibusVelocidade, OnibusVelocidadeCoordenadas

admin.site.register(OnibusLotacao)
admin.site.register(OnibusPosicao)
admin.site.register(OnibusVelocidade)
admin.site.register(OnibusVelocidadeCoordenadas)