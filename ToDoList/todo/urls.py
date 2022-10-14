from django.urls import path

from .views import IndexView, CreateToDoView, todo_detail_view, todo_done

app_name = 'todo'


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-todo/', CreateToDoView.as_view(), name='create-view'),
    path('todo/<int:pk>/', todo_detail_view, name='detail-view'),
    path('todo/<int:pk>/done', todo_done, name='todo-done')

]