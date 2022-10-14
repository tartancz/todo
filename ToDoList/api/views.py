from django.db.models import Q
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)
from rest_framework.viewsets import GenericViewSet

from todo.models import ToDo
from user.models import Profile
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnlyToDO, IsOwnerOrReadOnlyProfile
from .serializers import (
    ProfileSerializer,
    ProfileSerializerOwner,
    CommentSerializer,
    ToDoSerializer,
)


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet
                     ):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsOwnerOrReadOnlyProfile]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=['get', 'delete'], permission_classes=[IsAuthenticated])
    def logged(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'DELETE':
            user.delete()
            return Response({'info': f'account {user.username} was deleted'}, status=HTTP_200_OK)
        else:
            return Response(ProfileSerializer(instance=user.profile, context={'request': self.request}).data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def generate_token(self, request, *args, **kwargs):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'info': 'remember it, u cant access this token anymore, only create new'})


class ToDoViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet
                  ):
    serializer_class = ToDoSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnlyToDO,
    ]
    pagination_class = StandardResultsSetPagination


    def perform_create(self, serializer):
        todo = serializer.save(created_by=self.request.user)
        return todo

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly])
    def comment(self, request, *args, **kwargs):
        comment = CommentSerializer(data=request.data, context={'request': request})
        if comment.is_valid():
            todo = self.get_object()
            comment.save(created_by=request.user, created_in=todo)
            return Response(comment.data)
        return Response({'detail': 'Bad request'}, status=HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ToDo.objects.filter(Q(public=True) | Q(created_by=user))
        else:
            return ToDo.objects.filter(public=True)
