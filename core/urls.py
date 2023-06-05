"""
Urls for user role app.
"""
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    CreateUserView,
    UserMangerView,
    LoginUserView,
    LogoutUserView,
)

from .middlewares import (
    auth_middleware,
    flask_swagger,
)
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('user', UserMangerView)

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    path('login_user/', LoginUserView.as_view(), name='login-user'),
    path('logout_user/', LogoutUserView.as_view(), name='logout-user'),
    path('user/', UserMangerView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('authenticate/', auth_middleware, name='auth-middleware'),

    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('docs/strategy/', flask_swagger, name='flask-swagger'),
]
