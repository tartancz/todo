import pytest

from todo.models import ToDo, Comment
from todo.tests.factories import ToDoFactory, CommentFactory


@pytest.mark.django_db
def test_models_to_str():
    todo = ToDoFactory()
    comment = CommentFactory()
    assert str(todo) == todo.title
    assert str(comment) == f"by {comment.created_by} in {comment.created_on}"

