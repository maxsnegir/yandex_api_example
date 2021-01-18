from uuid import uuid4

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAdmin
from users.serializers import EmailSerializer, JWTSerializer, UserSerializer
from users.utils import get_token_for_user, send_email

User = get_user_model()


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = EmailSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.data['email'])
        user.confirmation_code = uuid4()
        user.save()
        send_email(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def get_jwt_token(request):
    serializer = JWTSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, email=serializer.data['email'])
        return Response(get_token_for_user(user),
                        status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    lookup_field = 'username'
    http_method_names = [u'get', u'post', u'patch', u'delete', ]


class MeAPIView(RetrieveUpdateAPIView, ):
    permission_classes = (IsAuthenticated,)
    http_method_names = [u'get', u'patch']

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
