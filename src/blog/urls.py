from django.urls import path
from .views import category_list, post_list, post_create, post_detail, post_get_update_delete
#from .views import comment_list

urlpatterns = [
    path("category-list/", category_list),
    path("post-list/", post_list),
    path("post-create/", post_create),
    path("<str:slug>/post-detail/", post_detail),
    #path("comment-list/", comment_list),
    path("<str:slug>/edit/", post_get_update_delete, name="update"),
]
