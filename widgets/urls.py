from django.urls import path

from widgets.views import (
    WidgetListView,
    WidgetDetailView,
    CommentCreateView,
    CommentUpdateView,
)

app_name = "widgets"

urlpatterns = [
    path("", WidgetListView.as_view(), name="index"),
    path("<uuid:pk>", WidgetDetailView.as_view(), name="detail"),
    path("<uuid:pk>/create", CommentCreateView.as_view(), name="comment_create"),
    path("<uuid:pk>/update", CommentUpdateView.as_view(), name="comment_update"),
]

