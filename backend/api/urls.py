from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalHouseViewSet
from django.contrib import admin
from django.urls import path, include
from .views import RentalHouseViewSet, user_signup, user_login, admin_login

router = DefaultRouter()
router.register('houses', RentalHouseViewSet, basename='rentalhouse' )

urlpatterns = [
    path('', include(router.urls)),  # /api/houses/ and /api/houses/<id>/

    # Auth routes

           
    path("signup/", user_signup, name="user-signup"),   # /api/signup/
    path("login/", user_login, name="user-login"),      # /api/login/
    path("admin-login/", admin_login, name="admin-login"), # /api/admin-login/
 
    
]
