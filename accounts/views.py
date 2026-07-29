from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

from posts.models import Post

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Registration successful. You can now log in."
            )

            return redirect("login")

    else:
        form = UserRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect("post_list")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()          
            login(request, user)
            next_url = request.GET.get("next")
            if next_url:
                return redirect(next_url)          
            messages.success(request, "Welcome back!")
            return redirect("post_list")
    else:
        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )
    
def author_profile(request, username):
    author = get_object_or_404(
        User.objects.select_related("profile"),
        username=username,
    )

    posts = (
        Post.objects.filter(
            author=author,
            status=Post.Status.PUBLISHED,
        )
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )

    context = {
        "author": author,
        "posts": posts,
    }

    return render(
        request,
        "accounts/author_profile.html",
        context,
    )