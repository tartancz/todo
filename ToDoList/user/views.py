from random import randint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView
from django.db.models import Q
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.db import transaction

from .forms import (
    UserModifiedCreationForm,
    ProfileCreationForm,
    UserModifiedUpdateForm,
    ProfileUpdateForm,
)
from .models import Profile
from todo.models import ToDo


# Create your views here.


class LoginModifiedView(LoginView):
    template_name = "user/auth/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponsePermanentRedirect(reverse("todo:index"))
        return super(LoginModifiedView, self).dispatch(request, *args, **kwargs)


@transaction.atomic
def register_view(request):
    if request.user.is_authenticated:
        return HttpResponsePermanentRedirect(reverse("todo:index"))
    user_form = UserModifiedCreationForm(request.POST or None)
    profile_form = ProfileCreationForm(request.POST or None)
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    if request.method == "GET":
        return render(request, template_name="user/auth/register.html", context=context)
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponsePermanentRedirect(reverse("login"))
        return render(
            request,
            template_name="user/auth/register.html",
            context=context,
            status=HTTP_400_BAD_REQUEST,
        )


class ProfileView(DetailView):
    model = Profile
    template_name = "user/logged/profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        # BASE
        if self.request.user.is_authenticated:
            context['base'] = 'user/logged/user_logged_base.html'
        else:
            context['base'] = 'user/auth/user_auth_base.html'
        # TODOS LIST
        todo_owner = self.get_object().user
        if self.request.user == todo_owner:
            context['todos'] = ToDo.objects.filter(created_by_id=self.kwargs['pk'])
        else:
            context['todos'] = ToDo.objects.filter(Q(created_by_id=self.kwargs['pk']) & Q(public=True))
        return context


@login_required()
def update_profile_view(request):
    user_form = UserModifiedUpdateForm(
        request.POST or None,
        instance=request.user,
    )
    profile_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user.profile,
    )
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    if request.method == "GET":
        return render(
            request, template_name="user/logged/update_profile.html", context=context
        )
    if request.method == "POST":
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponsePermanentRedirect(
                reverse("profile", args=[request.user.id])
            )
        return render(
            request,
            template_name="user/logged/update_profile.html",
            context=context,
            status=400,
        )


@login_required()
def delete_profile(request):
    if request.method == "GET":
        number = randint(1000, 9999)
        request.user.profile.delete_number = number
        request.user.profile.save()
        context = {"random": number}
        return render(
            request, template_name="user/logged/delete_profile.html", context=context
        )
    if request.method == "POST":
        context = {"random": request.user.profile.delete_number}
        if str(request.user.profile.delete_number) == request.POST.get("number"):
            request.user.delete()
            return HttpResponsePermanentRedirect(reverse("register"))
        return render(
            request,
            template_name="user/logged/delete_profile.html",
            context=context,
            status=HTTP_400_BAD_REQUEST,
        )
