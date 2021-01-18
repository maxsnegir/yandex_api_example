from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Title(models.Model):
    name = models.CharField(max_length=255)
    year = models.PositiveIntegerField(blank=True, null=True)
    rating = models.PositiveIntegerField(validators=[
        validators.MaxValueValidator(10, )], blank=True, null=True, )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField('Genre', blank=True, )
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Comment(models.Model):
    review = models.ForeignKey('Review', on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author}'

    class Meta:
        ordering = ['pub_date']


class Review(models.Model):
    SCORES = (
        (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
        (8, 8), (9, 9),
        (10, 10)
    )

    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(choices=SCORES, )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_author'),
        ]
        ordering = ['pub_date']

    def __str__(self):
        return f"By {self.author} to {self.title}"
