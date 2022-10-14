from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ProfileViewSet, ToDoViewSet

router = DefaultRouter()
router.register('profile', ProfileViewSet, basename='profile')
router.register('todo', ToDoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),

]