from django.conf import settings
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from users.forms import Userloginform, UserRegistrationForm, UserProfileForm, UserProfileChangeForm
from django.contrib import messages
from baskets.models import Basket
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from users.models import User


def send_verify_mail(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портaлe {settings.DOMAIN_NAME} ' \
              f'Пройдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


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
            user = form.save()
            if send_verify_mail(user):
                messages.success(request, 'Сообщение отправлено!')
                return HttpResponseRedirect(reverse('users:login'))
            else:
                messages.success(request, 'Сообщение не отправлено!')
                return HttpResponseRedirect(reverse('users:login'))
        else:
            return HttpResponseRedirect(reverse('users:registration'))
    form = UserRegistrationForm()
    context = {'title': 'Geekshop - регистрация', 'form': form}
    return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


@transaction.atomic
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileChangeForm(data=request.POST, instance=request.user.userprofileinf)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileChangeForm(instance=request.user.userprofileinf)

    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'GeekShop - Профиль',
        'baskets': Basket.objects.filter(user=request.user), }

    return render(request, 'users/profile.html', context)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expires():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'users/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'users/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))
