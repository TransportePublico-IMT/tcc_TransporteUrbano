from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from panel import plots, views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    # AUTH
    path("cadastro", views.SignUp.as_view(), name="cadastro"),
    path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    # DASH PLOTLY
    path("django_plotly_dash/", include("django_plotly_dash.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
