from .models import ToDo, Comment
from django import forms


class ToDoForm(forms.ModelForm):
    dead_line = forms.DateTimeField(
        required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local"})
    )

    class Meta:
        model = ToDo
        fields = ["title", "description", "dead_line", "public"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {
            "text" : "You can add comment"
        }

