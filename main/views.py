from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, status, permissions
from rest_framework.response import Response

from main.models import Category, Genre, Title, Review
from main.permissions import CommentGenrePermission, TitlePermission, \
    ReviewCommentPermission
from main.serializers import CategorySerializer, GenreSerializer, \
    TitleSerializerPOST, ReviewSerializer, TitleSerializerGET, \
    CommentSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [CommentGenrePermission, ]
    http_method_names = [u'get', u'post', u'delete']
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    http_method_names = [u'get', u'post', u'delete']
    permission_classes = [CommentGenrePermission, ]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [TitlePermission, ]
    http_method_names = [u'get', u'post', u'delete', u'patch']

    def get_queryset(self):
        queryset = Title.objects.all()
        genre_slug = self.request.query_params.get('genre', None)
        category_slug = self.request.query_params.get('category', None)
        year = self.request.query_params.get('year', None)
        name = self.request.query_params.get('name', None)

        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        elif category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)
        elif year is not None:
            queryset = queryset.filter(year=year)
        elif name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return TitleSerializerGET
        return TitleSerializerPOST


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReviewCommentPermission, ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_update(self, serializer):
        serializer.save()
        self.set_rating(self.get_object().title)

    def perform_destroy(self, instance):
        instance.delete()
        self.set_rating(instance.title)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            title = get_object_or_404(Title, id=kwargs['title_id'])
            if not title.reviews.filter(author=request.user):
                serializer.save(title=title)
                self.set_rating(title)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED,)
            return Response({'author': 'Вы уже делали review для этого title'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def set_rating(self, title):
        rating = title.reviews.all().aggregate(Avg('score'))
        title.rating = rating['score__avg']
        title.save()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReviewCommentPermission, ]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'],
                                   title__id=self.kwargs['title_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        get_object_or_404(Title, id=self.kwargs['title_id'])
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        serializer.save(review=review)
