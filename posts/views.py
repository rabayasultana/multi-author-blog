from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Post, Category, Tag, Comment, Like
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CategoryForm, TagForm, CommentForm
from django.http import Http404



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

    return render(request, "posts/post_list.html", context)

# def post_detail(request, slug):
#     post = get_object_or_404(
#         Post.objects.select_related(
#             "author",
#             "category"
#         ).prefetch_related(
#             "tags",
#             "comments"
#         ),
#         slug=slug,
#     )

def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if (
        post.status == Post.Status.DRAFT
        and (
            not request.user.is_authenticated
            or (
                request.user != post.author
                and not request.user.is_superuser
            )
        )
    ):
        raise Http404()

    session_key = f"viewed_post_{post.id}"

    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(
            view_count=F("view_count") + 1
        )

        request.session[session_key] = True
        post.refresh_from_db()

    comments = post.comments.select_related(
        "author"
    ).order_by("created_at")
    
    user_has_liked = False

    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(
            post=post,
            user=request.user
        ).exists()

    context = {
    "post": post,
    "comments": comments,
    "comment_form": CommentForm(),
    "user_has_liked": user_has_liked,
}

    return render(
        request,
        "posts/post_detail.html",
        context
    )

    # # Only the author or admin can view draft posts
    # if post.status == Post.Status.DRAFT:
    #     if (
    #         not request.user.is_authenticated
    #         or (
    #             request.user != post.author
    #             and not request.user.is_superuser
    #         )
    #     ):
    #         raise Http404("Post not found")

    # session_key = f"viewed_post_{post.id}"

    # if not request.session.get(session_key):
    #     Post.objects.filter(pk=post.pk).update(
    #         view_count=F("view_count") + 1
    #     )

    #     request.session[session_key] = True

    #     post.refresh_from_db(fields=["view_count"])

    # return render(
    #     request,
    #     "posts/post_detail.html",
    #     {
    #         "post": post
    #     },
    # )
    
@login_required
def create_post(request):
    if not request.user.profile.is_author:
        messages.error(
            request,
            "You are not allowed to create blog posts."
        )
        return redirect("post_list")

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            form.save_m2m()

            messages.success(
                request,
                "Post created successfully."
            )

            return redirect("post_detail", slug=post.slug)

    else:
        form = PostForm()

    return render(
        request,
        "posts/create_post.html",
        {
            "form": form
        },
    )
    
    
@login_required
def create_category(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can create categories.")
        return redirect("post_list")

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect("post_list")

    else:
        form = CategoryForm()

    return render(
        request,
        "posts/create_category.html",
        {
            "form": form
        }
    )


@login_required
def create_tag(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admin can create tags.")
        return redirect("post_list")

    if request.method == "POST":
        form = TagForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Tag created successfully.")
            return redirect("post_list")

    else:
        form = TagForm()

    return render(
        request,
        "posts/create_tag.html",
        {
            "form": form
        }
    )
    
@login_required
def author_dashboard(request):
    if not request.user.profile.is_author:
        return redirect("post_list")

    posts = (
        request.user.posts
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    context = {
        "posts": posts,
    }

    return render(
        request,
        "posts/dashboard.html",
        context,
    )
    
from django.shortcuts import get_object_or_404


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        form = PostForm(
            request.POST,
            request.FILES,
            instance=post,
        )

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = PostForm(instance=post)

    return render(
        request,
        "posts/edit_post.html",
        {
            "form": form,
        },
    )
    
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("dashboard")

    if request.method == "POST":
        post.delete()
        return redirect("dashboard")

    return render(
        request,
        "posts/delete_post.html",
        {
            "post": post,
        },
    )
    
    
@login_required
def add_comment(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post
            comment.author = request.user

            comment.save()

    return redirect("post_detail", slug=slug)


@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if (
        request.user == comment.author
        or request.user == comment.post.author
        or request.user.is_superuser
    ):

        slug = comment.post.slug

        comment.delete()

        return redirect(
            "post_detail",
            slug=slug
        )

    return redirect("post_detail", slug=comment.post.slug)

@login_required
def toggle_like(request, slug):

    post = get_object_or_404(Post, slug=slug)

    like, created = Like.objects.get_or_create(
        post=post,
        user=request.user
    )

    if not created:
        like.delete()

    return redirect(
        "post_detail",
        slug=slug
    )