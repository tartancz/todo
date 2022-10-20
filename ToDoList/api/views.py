from django.db.models import Q
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.viewsets import GenericViewSet

from todo.models import ToDo
from user.models import Profile
from .pagination import StandardResultsSetPagination
from .permissions import IsOwnerOrReadOnlyToDO
from .serializers import (
    ProfileSerializer,
    ProfileSerializerOwner,
    CommentSerializer,
    ToDoSerializer,
)


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    For model Profile

    Cant acces your private information nor update it from here,you must use action logged to do it.

    In detail can be used pagination for todos (example: ?page_size=5&page=2)

    ACTION:
    Generate token -> will generate token to use api
    Logged -> access to your profile
    """

    queryset = Profile.objects.all()
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if "logged" in self.action:
            return ProfileSerializerOwner
        else:
            return ProfileSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def logged(self, request, *args, **kwargs):
        """
        For model Profile in u are logged

        Here u can use method PATCH to modifies fields: name, gender

        with Method DELETE u can delete your profile
        """
        ser_class = self.get_serializer_class()
        user = request.user
        return Response(
            ser_class(instance=user.profile, context={"request": self.request}).data
        )

    @logged.mapping.patch
    def logged_patch(self, request, *args, **kwargs):
        ser_class = self.get_serializer_class()
        user = request.user
        ser = ser_class(
            data=request.data,
            instance=user.profile,
            context={"request": self.request},
            partial=True,
        )
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=200)
        else:
            return Response({"detail": "bad request"}, status=400)

    @logged.mapping.delete
    def logged_delete(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response(
            {"info": f"account {user.username} was deleted"}, status=HTTP_200_OK
        )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def generate_token(self, request, *args, **kwargs):
        """
        will generate your sercet key to use.

        REMEMBER THIS TOKEN, CUZ U CANT ACCES HIM ANYMORE, only generate new

        Request auth must look like this "Token f02b72e39fef297e3d56c57441cf9f315e5d7587"
        """
        user = request.user
        if hasattr(user, "auth_token"):
            user.auth_token.delete()
        token = Token.objects.create(user=user)
        return Response(
            {
                "token": token.key,
                "info": "remember it, u cant access this token anymore, only create new",
            }
        )


class ToDoViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    """
    For model ToDo

    In detail can be used pagination for comments (example: ?page_size=5&page=2)

    ACTION:
    Generate token -> will generate token to use api
    Logged -> access to your profile
    """

    serializer_class = ToDoSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnlyToDO,
    ]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        todo = serializer.save(created_by=self.request.user)
        return todo

    @action(
        detail=True, methods=["post"], permission_classes=[IsAuthenticatedOrReadOnly]
    )
    def comment(self, request, *args, **kwargs):
        """
        will add comment
        """
        comment = CommentSerializer(data=request.data, context={"request": request})
        if comment.is_valid():
            todo = self.get_object()
            comment.save(created_by=request.user, created_in=todo)
            return Response(comment.data)
        return Response({"detail": "Bad request"}, status=HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["patch"], permission_classes=[IsOwnerOrReadOnlyToDO])
    def done(self, request, *args, **kwargs):
        """
        mark todo as completed
        """
        todo = self.get_object()
        todo.completed = True
        todo.save()
        ser = self.get_serializer_class()
        return Response(ser(instance=todo, context={"request": self.request}).data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ToDo.objects.filter(Q(public=True) | Q(created_by=user))
        else:
            return ToDo.objects.filter(public=True)
