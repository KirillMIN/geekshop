from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
# Create your views here.
from users.forms import Userloginform, UserRegistrationForm, UserProfileForm
from django.contrib import messages
from baskets.models import Basket
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == 'POST':
        form = Userloginform(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = Userloginform()
    context = {'title': 'GeekShop - Авторизация', 'form': form, 'baskets': Basket.objects.all()}
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'вы успешно зарегестрировались!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return HttpResponseRedirect(reverse('users:registration'))
    form = UserRegistrationForm()
    context = {'title': 'Geekshop - регистрация', 'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
    context = {'title': 'GeekShop - Личный кабинет', 'form': form, 'baskets': Basket.objects.filter(user=request.user)}
    return render(request, 'users/profile.html', context)