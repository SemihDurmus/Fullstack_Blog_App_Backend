from django.forms import ModelForm
from .models import Comment, Like


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = (
            "commenter",
            "post",
            "content"
        )
