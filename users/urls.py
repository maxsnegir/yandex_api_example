from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('users', views.UsersViewSet, basename='users')

urlpatterns = [
    path('v1/users/me/', views.MeAPIView.as_view()),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/email/', views.get_confirmation_code),
    path('v1/auth/token/', views.get_jwt_token),

]
