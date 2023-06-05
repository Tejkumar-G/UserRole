"""
User Role app views
"""
from django.contrib.auth import get_user_model
from rest_framework import (
    mixins,
    viewsets,
    permissions,
    status,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    UserSerializer,
    LoginUserSerializer,
)


class CreateUserView(APIView):
    """This view for creating user."""
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            user = get_user_model().objects.get(pk=serializer.data['id'])
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )




class LoginUserView(APIView):
    """This view is for user login."""
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )

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
