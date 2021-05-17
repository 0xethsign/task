from django.http.response import HttpResponseBadRequest
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm, EditFileName
from .models import Image
import cv2
import pytesseract


@login_required
def home(request):
    context = {}

    if request.method == "POST":
        print(request.user)
        form = UploadFileForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            username = request.user
            image_text = request.FILES["image"].name
            image = form.cleaned_data.get("image")
            # extracting text from image
            print('----------------------')
            # image_clone = '../media/storage/'+str(image)
            image_clone = cv2.imread(str(image))
            print(str(image))
            print('----------------------')
            image_clone = cv2.cvtColor(image_clone, cv2.COLOR_BGR2GRAY)
            image_clone = cv2.threshold(
                image_clone, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            image_clone = cv2.medianBlur(image_clone, 5)
            OCRtext = pytesseract.image_to_string(image_clone)
            obj = Image.objects.create(
                username=username,
                image_text=image_text,
                image=image,
                OCRtext=OCRtext
            )
            obj.save()
            print(obj)
    else:
        form = UploadFileForm()
        form2 = EditFileName()
        context['form2'] = form2
    context['form'] = form
    context['data'] = Image.objects.all()
    print(context)
    return render(request, "registration/success.html", context)


def edit(request):
    context = {}
    if request.method == "POST":
        print('--------------')
        form2 = EditFileName(request.POST)
        if form2.is_valid():
            username = request.user
            image_text = form2.cleaned_data.get("image_text")
            obj = Image.objects.filter(id=request.POST['image_id']).update(
                image_text=image_text
            )

            print('obj in form2', obj)
    form2 = EditFileName()
    context['form2'] = form2
    form = UploadFileForm()
    context['form'] = form
    context['data'] = Image.objects.all()
    print(context)
    return redirect('/home/')


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
