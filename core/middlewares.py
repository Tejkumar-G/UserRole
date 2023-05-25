"""
Middle wares for the other microservices.
"""
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def auth_middleware(request):
    """This was middleware api to check if the user was authenticated."""

    # Validate the token using Django Rest Framework's Token model
    try:
        user = get_user_from_token(request)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=401)

    return Response({'user_id': user.id})


def get_user_from_token(request):
    # Create an instance of JWTAuthentication
    jwt_authentication = JWTAuthentication()

    # Authenticate the request and retrieve the user object
    try:
        user, _ = jwt_authentication.authenticate(request)
        # Now you have the user object and can perform any necessary operations
        return user
    except:
        # Handle the case where the token is invalid or expired
        # Return an error response or perform appropriate actions
        return None
