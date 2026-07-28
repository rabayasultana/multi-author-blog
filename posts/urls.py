from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.post_list_view, name="post_list"),
    path(
        "post/<slug:slug>/",
        views.post_detail,
        name="post_detail"
    ),
    path(
        "create/",
        views.create_post,
        name="create_post",
    ),
    path(
        "category/create/",
        views.create_category,
        name="create_category",
    ),
    path(
        "tag/create/",
        views.create_tag,
        name="create_tag",
    ),
    path(
        "dashboard/",
        views.author_dashboard,
        name="dashboard",
    ),
    path(
    "edit/<int:pk>/",
    views.edit_post,
    name="edit_post",
    ),

    path(
        "delete/<int:pk>/",
        views.delete_post,
        name="delete_post",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )