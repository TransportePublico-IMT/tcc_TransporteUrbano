from rest_framework.viewsets import ModelViewSet
from onibus.models import Onibus
from .serializers import OnibusSerializer 

class OnibusViewSet(ModelViewSet):
    queryset = Onibus.objects.all()
    serializer_class = OnibusSerializer