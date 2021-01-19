from django.db import models
from django.contrib.auth.models import User
import json


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def post_count(self):
        return self.post_set.count()
        # _set is to reach a value of a child from parent


class Post(models.Model):
    OPTIONS = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_URL = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    author_avatar = models.CharField(
        max_length=220, default="https://www.kindpng.com/picc/m/105-1055656_account-user-profile-avatar-avatar-user-profile-icon.png")
    status = models.CharField(max_length=10, choices=OPTIONS, default="draft")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comment_set.all().count()

    def like_count(self):
        return self.like_set.all().count()

    def view_count(self):
        return self.postview_set.all().count()

    # def comments(self):
    #     return self.comment_set.all()


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.commenter.username


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
