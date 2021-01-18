from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenresViewSet, basename='genres')
router_v1.register('titles', views.TitlesViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
                   basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
