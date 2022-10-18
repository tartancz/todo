from django.db.models import Q
from rest_framework import serializers
from rest_framework.reverse import reverse

from api.utils import get_paginated_nested_serializer
from todo.models import ToDo, Comment
from user.models import Profile, Gender
from .custom_fields import ShowFieldChangeSlugFieldRelatedField


class NestedProfileSerializerInComment(serializers.ModelSerializer):
    profile_pic = serializers.ImageField()
    profile_api = serializers.SerializerMethodField('link_api', read_only=True)
    profile_web = serializers.SerializerMethodField('link_web', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'profile_pic', 'profile_api', 'profile_web']

    def link_api(self, instance):
        request = self.context.get('request')
        return reverse('profile-detail', args=[instance.id], request=request)

    def link_web(self, instance):
        request = self.context.get('request')
        return reverse('profile', args=[instance.id], request=request)


class CommentSerializer(serializers.ModelSerializer):
    created_on = serializers.ReadOnlyField(read_only=True)
    created_by = NestedProfileSerializerInComment(source='created_by.profile', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_on', 'created_by']


class ToDoSerializer(serializers.ModelSerializer):
    created_on = serializers.ReadOnlyField()
    created_by_api = serializers.HyperlinkedRelatedField(view_name='profile-detail', read_only=True,
                                                         source='created_by')
    created_by_web = serializers.HyperlinkedRelatedField(view_name='profile', read_only=True, source='created_by')
    comments = serializers.SerializerMethodField('comment')
    url = serializers.HyperlinkedIdentityField(view_name='todo-detail')

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'description', 'created_on', 'created_by_api', 'created_by_web', 'public', 'dead_line',
                  'completed', 'url',
                  'comments']

    def comment(self, instance):
        request = self.context.get('request')
        query_set = instance.comments_in.all()
        return get_paginated_nested_serializer(request, CommentSerializer, query_set)

    def get_fields(self):
        fields = super(ToDoSerializer, self).get_fields()
        if self.context.get('request').parser_context['view'].action == 'list':
            fields.pop('comments')
        return fields


class NestedTodoInProfile(serializers.ModelSerializer):
    todo_api = serializers.SerializerMethodField('link_api', read_only=True)
    todo_web = serializers.SerializerMethodField('link_web', read_only=True)

    class Meta:
        model = ToDo
        fields = ['todo_api', 'todo_web']

    def link_api(self, instance):
        request = self.context.get('request')
        return reverse('todo-detail', args=[instance.id], request=request)

    def link_web(self, instance):
        request = self.context.get('request')
        return reverse('todo:detail-view', args=[instance.id], request=request)


class ProfileSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField()
    todo = serializers.SerializerMethodField('to_do_list', read_only=True)
    gender = serializers.StringRelatedField(source='gender.gender_name')
    profile_api = serializers.SerializerMethodField('link_api', read_only=True)
    profile_web = serializers.SerializerMethodField('link_web', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'profile_pic', 'gender', 'profile_api', 'profile_web', 'todo']

    def get_fields(self):
        fields = super(ProfileSerializer, self).get_fields()
        if self.context.get('request').parser_context['view'].action == 'list':
            fields.pop('todo')
        return fields

    def to_do_list(self, instance):
        request = self.context.get('request')
        queryset = ToDo.objects.filter(Q(public=True) & Q(created_by=instance.user))

        return get_paginated_nested_serializer(request, NestedTodoInProfile, queryset)

    def link_api(self, instance):
        request = self.context.get('request')
        return reverse('profile-detail', args=[instance.id], request=request)

    def link_web(self, instance):
        request = self.context.get('request')
        return reverse('profile', args=[instance.id], request=request)


class ProfileSerializerOwner(ProfileSerializer):
    gender = ShowFieldChangeSlugFieldRelatedField(slug_field='pk', queryset=Gender.objects.all())
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta(ProfileSerializer.Meta):
        fields = ['id', 'name', 'username', 'email', 'profile_pic', 'gender', 'profile_api', 'profile_web', 'todo']

    def to_do_list(self, instance):
        request = self.context.get('request')
        user = request.user
        queryset = ToDo.objects.filter(created_by=user)
        return get_paginated_nested_serializer(request, NestedTodoInProfile, queryset)
