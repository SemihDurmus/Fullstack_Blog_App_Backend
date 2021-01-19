from django.urls import path
from .views import category_list, post_list_create, comment_list, post_get_update_delete

urlpatterns = [
    path("category-list/", category_list),
    path("post-list-create/", post_list_create),
    path("comment-list/", comment_list),
    path("<str:slug>/edit/", post_get_update_delete, name="update"),
]
