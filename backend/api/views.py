from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import RentalHouse
from .serializers import RentalHouseSerializer

class RentalHouseViewSet(ModelViewSet):
    queryset = RentalHouse.objects.all()
    serializer_class = RentalHouseSerializer
