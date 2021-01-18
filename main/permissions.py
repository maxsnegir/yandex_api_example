from rest_framework import permissions
from rest_framework.permissions import BasePermission


class CommentGenrePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'admin' or request.user.is_superuser


class ReviewCommentPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or (
                request.user.role == 'moderator' or request.user.is_superuser)

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class TitlePermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_superuser)
