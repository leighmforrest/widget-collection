from django.views.generic import ListView

from widgets.models import Widget


class WidgetListView(ListView):
    template_name = "widgets/index.html"
    context_object_name = "widgets"
    model = Widget
    paginate_by = 6

