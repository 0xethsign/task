from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, EditFileName
from .models import Image


@login_required
def home(request):
    context = {}
    if request.method == "PUT":
        form2 = EditFileName(request, request.FILES)
        if form2.is_valid():
            username = request.user
    if request.method == "POST":
        print(request.user)
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            username = request.user
            image_text = request.FILES["image"].name
            image = form.cleaned_data.get("image")
            obj = Image.objects.create(
                username=username,
                image_text=image_text,
                image=image
            )
            obj.save()
            print(obj)
    else:
        form = UploadFileForm()
    context['form'] = form
    context['data'] = Image.objects.all()
    print(context)
    return render(request, "registration/success.html", context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
