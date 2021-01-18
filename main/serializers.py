from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Category, Genre, Title, Review, Comment

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ['id']


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ['rating', ]


class TitleSerializerGET(TitleSerializer):
    genre = GenreSerializer(many=True, )
    category = CategorySerializer()


class TitleSerializerPOST(TitleSerializer):
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=False)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=User.objects.all(),
                                          default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username',
                                          queryset=User.objects.all(),
                                          default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['review', 'author']
