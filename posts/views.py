from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F

from .models import Post, Category, Tag


# def home(request):
#     posts = (
#         Post.objects.filter(status=Post.Status.PUBLISHED)
#         .select_related("author", "category")
#         .prefetch_related("tags")
#     )

#     search = request.GET.get("search")

#     if search:
#         posts = posts.filter(
#             Q(title__icontains=search) |
#             Q(content__icontains=search)
#         )

#     category = request.GET.get("category")

#     if category:
#         posts = posts.filter(category__id=category)

#     tag = request.GET.get("tag")

#     if tag:
#         posts = posts.filter(tags__id=tag)

#     paginator = Paginator(posts.distinct(), 5)

#     page_number = request.GET.get("page")

#     page_obj = paginator.get_page(page_number)

#     context = {
#         "page_obj": page_obj,
#         "categories": Category.objects.all(),
#         "tags": Tag.objects.all(),
#         "search": search,
#     }

#     return render(request, "blog/home.html", context)

def post_list_view(request):
    posts = (
        Post.objects.filter(status=Post.Status.PUBLISHED)
        .select_related("author", "category")
        .prefetch_related("tags")
    )

    search = request.GET.get("search")

    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    category = request.GET.get("category")

    if category:
        posts = posts.filter(category__id=category)

    tag = request.GET.get("tag")

    if tag:
        posts = posts.filter(tags__id=tag)

    paginator = Paginator(posts.distinct(), 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "search": search,
    }

    return render(request, "post_list.html", context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related(
            "author",
            "category"
        ).prefetch_related(
            "tags",
            "comments"
        ),
        slug=slug,
        status=Post.Status.PUBLISHED,
    )

    session_key = f"viewed_post_{post.id}"

    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(
            view_count=F("view_count") + 1
        )

        request.session[session_key] = True

        post.refresh_from_db(fields=["view_count"])

    context = {
        "post": post
    }

    return render(
        request,
        "post_detail.html",
        context,
    )