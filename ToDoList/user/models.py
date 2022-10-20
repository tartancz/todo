from django.db import models
from django.contrib.auth.models import User
import uuid

from PIL import Image


# Create your models here.


class Gender(models.Model):
    gender_name = models.CharField("gender", max_length=50)

    def __str__(self):
        return self.gender_name

    class Meta:
        ordering = ["id"]


class Profile(models.Model):
    name = models.CharField(
        "name", max_length=30, unique=False, help_text="name, required, max length=30"
    )
    profile_pic = models.ImageField(
        "profile picture",
        default="profile_pics/default_profile.jpg",
        upload_to="profile_pics/users",
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    delete_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)

    class Meta:
        ordering = ["id"]
