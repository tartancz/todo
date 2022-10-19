from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, FormView
from django.contrib.auth.views import redirect_to_login

from .forms import ToDoForm, CommentForm
from .models import ToDo


class IndexView(ListView):
    template_name = "todo/index.html"
    context_object_name = "list"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return ToDo.objects.filter(Q(created_by=self.request.user) | Q(public=True))
        else:
            return ToDo.objects.filter(public=True)


class CreateToDoView(LoginRequiredMixin, FormView):
    form_class = ToDoForm
    template_name = "todo/create_todo.html"
    success_url = reverse_lazy("todo:index")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        return super().form_valid(form)


def todo_detail_view(request, pk):
    comment_form = CommentForm(request.POST or None)
    if request.user.is_authenticated:
        # get object where pk is main para and is created by logged user or is public
        todo = get_object_or_404(
            ToDo, (Q(created_by=request.user) | Q(public=True)) & Q(pk=pk)
        )
    else:
        todo = get_object_or_404(ToDo, (Q(pk=pk) & Q(public=True)))
    if request.method == "GET":
        context = {}
        context["obj"] = todo

        context['comments'] = todo.comments_in.all()[:10]
        context["comment_form"] = comment_form
        return render(request, template_name="todo/detail_view.html", context=context)
    elif request.method == "POST":
        if request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.created_by = request.user
            comment.created_in = get_object_or_404(ToDo, pk=pk)
            comment.save()
            return HttpResponseRedirect(reverse("todo:detail-view", args=[pk]))
        else:
            return redirect_to_login(reverse("todo:detail-view", args=[pk]))


def todo_done(request, pk):
    todo = get_object_or_404(ToDo, pk=pk)
    if request.user == todo.created_by:
        todo.completed = True
        todo.save()
        return HttpResponseRedirect(reverse("todo:detail-view", args=[pk]))
    else:
        return HttpResponseForbidden()
