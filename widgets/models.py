import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Widget(BaseModel):
    name = models.CharField(max_length=256)
    curator = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="widgets"
    )

    class Meta:
        permissions = [("curator", "create update and delete widgets")]
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("widgets:detail", kwargs={"pk": self.pk})


class Comment(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    widget = models.ForeignKey(
        Widget, on_delete=models.CASCADE, related_name="comments"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        n = len(self.comment)
        if n > 75:
            return self.comment[:75] + "..."
        return self.comment


class Note(BaseModel):
    text = models.CharField(max_length=128)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.text

