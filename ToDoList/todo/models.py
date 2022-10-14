from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.


class ToDo(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    created_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todos")
    public = models.BooleanField(default=False)
    dead_line = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.CharField(max_length=120)
    created_on = models.DateTimeField(default=now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_in = models.ForeignKey(
        ToDo, on_delete=models.CASCADE, related_name="comments_in"
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"by {self.created_by} in {self.created_on}"
