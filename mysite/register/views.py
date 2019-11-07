from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import RegisterForm


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Success! You have created account <{username}>, please log in now.')
            return redirect("/ehealth/login")
    else:
        form = RegisterForm()
    return render(request, "register/register.html",{"form":form})
