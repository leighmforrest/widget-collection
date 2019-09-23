from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import PermissionDenied


from widgets.models import Widget, Comment
from widgets.forms import CommentForm


class WidgetListView(ListView):
    template_name = "widgets/index.html"
    context_object_name = "widgets"
    model = Widget
    paginate_by = 6


class WidgetDetailView(DetailView):
    template_name = "widgets/detail.html"
    context_object_name = "widget"
    model = Widget


class CommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "widgets/comment_create.html"
    model = Widget
    form_class = CommentForm
    success_message = "The comment has been created."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["widget"] = Widget.objects.get(pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        return Widget.objects.get(pk=self.kwargs["pk"]).get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.widget = Widget.objects.get(pk=self.kwargs["pk"])
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "widgets/comment_update.html"
    model = Comment
    form_class = CommentForm
    success_message = "The comment has been updated."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["widget"] = Comment.objects.get(pk=self.kwargs["pk"]).widget
        return context

    def get_success_url(self):
        comment = self.get_object()
        return comment.widget.get_absolute_url()

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.widget = Comment.objects.get(pk=self.kwargs["pk"]).widget
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class CommentDeleteView(DeleteView):
    model = Comment
    context_object_name = "comment"
    template_name = "widgets/comment_delete.html"

    def get_success_url(self):
        comment = self.get_object()
        return comment.widget.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        message = f"The comment has been deleted."
        messages.warning(self.request, message)
        return super().delete(request, *args, **kwargs)
