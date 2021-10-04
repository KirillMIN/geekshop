from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from products.models import Product
from users.models import User
from admins.forms import UserAdminRegistrationForm, UserAdminProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
# Create your views here.


@user_passes_test(lambda u: u.is_staff)
def index(request):
    context = {'title': 'Geekshop-admin'}
    return render(request, 'admins/index.html', context)

"""

@user_passes_test(lambda u: u.is_staff)
def admins_users(request):
    context = {'title': 'Geekshop-users', 'users': User.objects.all()}
    return render(request, 'admins/admin_users.html', context)
"""


class UserListView(ListView):
    model = User
    template_name = 'admins/admin_users.html'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Админ | Пользователи'
        return context

    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)

"""
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
"""


class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin_users_create.html'
    form_class = UserAdminRegistrationForm
    success_url = reverse_lazy('admins:admins_users')


class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_users')

"""
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
"""


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin_users_update_delete.html'
    success_url = reverse_lazy('admins:admins_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        return HttpResponseRedirect(self.get_success_url())


class ProductsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'admins/product_list.html'
    success_url = reverse_lazy('admins:admin_users')
