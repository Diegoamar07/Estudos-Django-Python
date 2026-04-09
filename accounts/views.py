from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_not_required


def register_view(request):
    
    if request.method == "POST":
        user_form = UserCreationForm(data=request.POST)

        if user_form.is_valid():
            user_form.save()
            return redirect("login")

    else:
        user_form = UserCreationForm()
        

    return render(
        request,
        "register.html",
        {"user_form": user_form}
    )


@login_not_required
def login_view(request):

    if request.method == "POST":
        user_form = AuthenticationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.get_user()
            login(request, user)
            return redirect("balcao_list")

    else:
        user_form = AuthenticationForm()


    return render(
        request,
        "login.html",
        {"user_form": user_form}
    )


def logout_view(request):

    logout(request)
    return redirect("login")
