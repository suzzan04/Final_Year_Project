from rest_framework import serializers
from .models import RentalHouse

class RentalHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalHouse
        fields = "__all__"
