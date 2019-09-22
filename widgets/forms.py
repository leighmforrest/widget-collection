from django import forms

from widgets.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("comment",)

    def clean_comment(self):
        data = self.cleaned_data["comment"]
        length = len(data)
        if length > 1024:
            raise forms.ValidationError("The comment is too long.")

        return data
