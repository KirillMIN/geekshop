from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Geekshop-admin'}
    return render(request, 'admins/index.html', context)


@user_passes_test(lambda u: u.is_staff)
def admins_users(request):
    context = {'title': 'Geekshop-users', 'users': User.objects.all()}
    return render(request, 'admins/admin_users.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_create(request):
    if request.method == 'POST':
        form = UserAdminRegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admins_users'))
    else:
        form = UserAdminRegistrationForm()
    context = {'title': 'Geekshop - Создание пользователя', 'form': form}
    return render(request, 'admins/admin_users_create.html', context)


@user_passes_test(lambda u: u.is_staff)
def create_user_update(request, id):
    selected_user = User.objects.get(id=id)
    if request.method == 'POST':
        form = UserAdminProfileForm(instance=selected_user, files=request.FILES, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admins:admins_users'))
    else:
        form = UserAdminProfileForm(instance=selected_user)
    context = {'title': 'Geekshop - Редактирование пользователя', 'selected_user': selected_user, 'form': form}
    return render(request, 'admins/admin_users_update_delete.html', context)


@user_passes_test(lambda u: u.is_staff)
def admin_users_delete(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    return HttpResponseRedirect(reverse('admins:admins_users'))
