from django.urls import path

from widgets.views import WidgetListView, WidgetDetailView, CommentCreateView

app_name = "widgets"

urlpatterns = [
    path("", WidgetListView.as_view(), name="index"),
    path("<uuid:pk>", WidgetDetailView.as_view(), name="detail"),
    path("<uuid:pk>/create", CommentCreateView.as_view(), name="comment_create"),
]

