from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin


from widgets.models import Widget
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
