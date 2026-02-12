from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RentalHouseViewSet,
    user_signup,
    user_login,
    admin_login
)

router = DefaultRouter()
# Note: 'houses' matches the endpoint used in your React fetch calls
router.register(r"houses", RentalHouseViewSet, basename="rentalhouse")

urlpatterns = [
    # Houses CRUD (/api/houses/) AND Recommendations (/api/houses/{id}/recommend/)
    path("", include(router.urls)),   

    # Authentication
    path("signup/", user_signup, name="user-signup"),
    path("login/", user_login, name="user-login"),
    path("admin-login/", admin_login, name="admin-login"),
]