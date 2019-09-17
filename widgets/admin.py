from django.contrib import admin

from widgets.models import Widget, Note, Comment


class NoteInline(admin.TabularInline):
    model = Note


class CommentInline(admin.TabularInline):
    model = Comment


class WidgetAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [NoteInline, CommentInline]
    max_num = 5


admin.site.register(Widget, WidgetAdmin)
