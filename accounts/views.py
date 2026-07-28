from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

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