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
)

from .middlewares import auth_middleware
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', UserMangerView)

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create-user'),
    # path('login_user/', LoginUserView.as_view(), name='login-user'),
    path('', include(router.urls)),
    path('authenticate/', auth_middleware, name='auth-middleware'),

    path('login_user/', LoginUserView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
