from django.contrib import admin

from main.models import Category, Genre, Title, Review, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'category']


@admin.register(Review)
class ReviewTitleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'score']


@admin.register(Comment)
class CommentTitleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'pub_date']
