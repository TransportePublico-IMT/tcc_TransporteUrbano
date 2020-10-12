from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers

from climatempo.api.viewsets import ClimaTempoViewSet
from evento.api.viewsets import EventoViewSet
from linha.api.viewsets import LinhaViewSet
from onibus.api.viewsets import (
    OnibusLotacaoViewSet,
    OnibusPosicaoViewSet,
    OnibusVelocidadeViewSet,
)
from panel import plots, views
from parada.api.viewsets import ParadaViewSet
from trem.api.viewsets import TremViewSet

router = routers.DefaultRouter()
router.register("onibus-lotacao", OnibusLotacaoViewSet, basename="OnibusLotacao")
router.register("onibus-posicao", OnibusPosicaoViewSet, basename="OnibusPosicao")
router.register(
    "onibus-velocidade", OnibusVelocidadeViewSet, basename="OnibusVelocidade"
)
router.register("linhas", LinhaViewSet, basename="Linha")
router.register("paradas", ParadaViewSet, basename="Parada")
router.register("trens", TremViewSet, basename="Trem")
router.register("climatempo", ClimaTempoViewSet, basename="ClimaTempo")
router.register("eventos", EventoViewSet, basename="Evento")

urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("api/", include(router.urls)),
    # PAGES
    path("", views.home, name="home"),
    # AUTH
    path("cadastro", views.SignUp.as_view(), name="cadastro"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    # DASH PLOTLY
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
