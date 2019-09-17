from django.urls import path

from widgets.views import WidgetListView

app_name = "widgets"
urlpatterns = [path("", WidgetListView.as_view(), name="index")]

