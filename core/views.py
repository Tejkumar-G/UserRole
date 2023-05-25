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
    exceptions,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
)


class CreateUserView(APIView):
    """This view for creating user."""
    serializer_class = UserSerializer

    def post(self, request):
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
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class LoginUserView(TokenObtainPairView):
    """This view is for user login."""
    serializer_class = CustomTokenObtainPairSerializer



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
        obj = super().get_object()
        if obj.id != self.request.user.id:
            # Handle unauthorized access
            # For example, you can raise a permission denied exception
            raise exceptions.PermissionDenied("You are not allowed to access this user.")
        return obj
