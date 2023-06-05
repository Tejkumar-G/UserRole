"""
User Role app views
"""
from django.contrib.auth import (
    get_user_model,
)
from rest_framework import (
    mixins,
    viewsets,
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (
    UserSerializer,
)


class CreateUserView(APIView):
    """This view for creating user."""
    serializer_class = UserSerializer
    @staticmethod
    def post( request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            user = get_user_model().objects.get(pk=serializer.data['id'])
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginUserView(TokenObtainPairView):
    """This view is for user login."""
    serializer_class = TokenObtainPairSerializer

class LogoutUserView(APIView):
    """This view is for user logout."""
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request):
        refresh = RefreshToken.for_user(request.user)
        # Perform logout
        refresh.blacklist()

        return Response({"detail": "User logged out successfully."})

class UserMangerView(
            mixins.RetrieveModelMixin,
            mixins.UpdateModelMixin,
            mixins.DestroyModelMixin,
            viewsets.GenericViewSet,
            ):
    """This is view for retrieve, update, and delete the user."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

    def get_object(self):
        # obj = super().get_object()
        # if obj.id != self.request.user.id:
        #     # Handle unauthorized access
        #     # For example, you can raise a permission denied exception
        #     raise exceptions.PermissionDenied("You are not allowed to access this user.")
        return self.request.user
