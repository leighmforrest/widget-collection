from django.views.generic import ListView, DetailView

from widgets.models import Widget


class WidgetListView(ListView):
    template_name = "widgets/index.html"
    context_object_name = "widgets"
    model = Widget
    paginate_by = 6


class WidgetDetailView(DetailView):
    template_name = "widgets/detail.html"
    context_object_name = "widget"
    model = Widget
