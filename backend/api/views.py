from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import RentalHouse
from .serializers import RentalHouseSerializer

# Import your KNN function
try:
    from ai.knn_model import recommend_house
except ImportError:
    def recommend_house(**kwargs):
        return {"error": "AI model script not found"}

# -------------------- HOUSE CRUD & AI ACTION --------------------
class RentalHouseViewSet(ModelViewSet):
    queryset = RentalHouse.objects.all().order_by("-created_at")
    serializer_class = RentalHouseSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = RentalHouse.objects.all()
        # Get search parameters
        query = self.request.query_params.get("search")
        district = self.request.query_params.get("district")
        
        # Flexible Search (Title, Location, or District)
        if query:
            qs = qs.filter(
                Q(title__icontains=query) | 
                Q(location__icontains=query) | 
                Q(district__icontains=query)
            )
        
        if district:
            qs = qs.filter(district__icontains=district)

        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("❌ VALIDATION ERROR:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # NEW: AI Recommendation Action
    # Access this via: GET /api/houses/{id}/recommend/
    @action(detail=True, methods=['get'])
    def recommend(self, request, pk=None):
        house = self.get_object()
        
        try:
            # 1. Get similar items from KNN Model
            # We ignore 'posted_days' as per your request
            recommendations_data = recommend_house(
                price=float(house.price),
                beds=int(house.beds),
                baths=int(house.baths)
            )

            if isinstance(recommendations_data, dict) and "error" in recommendations_data:
                raise Exception(recommendations_data["error"])

            # 2. Extract unique identifiers (titles or IDs) from AI results
            # Assuming your CSV/Dataframe has a 'title' column
            rec_titles = [item['title'] for item in recommendations_data]

            # 3. Fetch these houses from our actual Database
            # We exclude the current house so it doesn't recommend itself
            results = RentalHouse.objects.filter(
                title__in=rec_titles
            ).exclude(id=house.id)[:5]

            # 4. Fallback: If AI finds nothing, suggest houses in the same district
            if not results.exists():
                results = RentalHouse.objects.filter(
                    district__icontains=house.district
                ).exclude(id=house.id)[:5]

        except Exception as e:
            print(f"⚠️ AI Error: {e}. Falling back to basic filtering.")
            # Fallback to simple database filtering if AI fails
            results = RentalHouse.objects.filter(
                district__icontains=house.district
            ).exclude(id=house.id)[:5]

        serializer = RentalHouseSerializer(results, many=True)
        return Response(serializer.data)


# -------------------- AUTHENTICATION --------------------

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

    return Response({
        "message": "Login successful",
        "role": "user",
        "username": user.username
    }, status=200)


@api_view(["POST"])
@permission_classes([AllowAny])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is None or not user.is_staff:
        return Response({"error": "Admin access denied"}, status=401)

    return Response({
        "message": "Admin login successful", 
        "role": "admin",
        "username": user.username
    }, status=200)