"""
Middle wares for the other microservices.
"""
from django.shortcuts import render
from rest_framework import exceptions
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['GET'])
@renderer_classes([JSONRenderer])
def auth_middleware(request):
    """Middleware API to check if the user is authenticated."""
    if 'Authorization' not in request.headers:
        return Response({'error': 'Missing authorization header'}, status=404)

    try:
        user = get_user_from_token(request)
    except exceptions.AuthenticationFailed:
        return Response({'error': 'Invalid token'}, status=401)

    return Response({'user_id': user.id})


def get_user_from_token(request):
    """Retrieve the user from the request header."""
    jwt_authentication = JWTAuthentication()

    # Authenticate the request and retrieve the user object
    user, _ = jwt_authentication.authenticate(request)

    if user is None:
        raise exceptions.AuthenticationFailed('Invalid token')

    return user



def flask_swagger(request):
    """It will render the flask application swagger."""
    return render(request, 'flask_swagger.html', {'flask_url': 'http://192.168.5.97:8001/'})
