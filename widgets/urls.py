from django.urls import path

from widgets.views import WidgetListView, WidgetDetailView

app_name = "widgets"

urlpatterns = [
    path("", WidgetListView.as_view(), name="index"),
    path("<uuid:pk>", WidgetDetailView.as_view(), name="detail"),
]

