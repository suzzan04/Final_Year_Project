from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .models import RentalHouse
from .serializers import RentalHouseSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class RentalHouseViewSet(ModelViewSet):
    queryset = RentalHouse.objects.all()
    serializer_class = RentalHouseSerializer
    def get_queryset(self):
        qs = RentalHouse.objects.all()

        city = self.request.query_params.get("city")
        house_type = self.request.query_params.get("house_type")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")

        if city:
            qs = qs.filter(city__icontains=city)

        if house_type:
            qs = qs.filter(house_type__icontains=house_type)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        return qs


@api_view(["POST"])
@permission_classes([AllowAny])
def user_signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username & password required"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=400)

    User.objects.create_user(username=username, password=password)
    return Response({"message": "Signup successful"}, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    return Response({"message": "Login successful", "role": "user"})

@api_view(["POST"])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None or not user.is_staff:
        return Response({"error": "Admin access denied"}, status=401)

    return Response({"message": "Admin login successful", "role": "admin"})

