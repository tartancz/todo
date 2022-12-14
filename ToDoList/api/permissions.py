from rest_framework import permissions

class IsOwnerOrReadOnlyToDO(permissions.BasePermission):
    '''
    permission for ToDoModel
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user

class IsOwnerOrReadOnlyProfile(permissions.BasePermission):
    '''
    permission for ToDoModel
    '''
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


