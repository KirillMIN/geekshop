from django.urls import path

from admins.views import index, admins_users, admin_users_create, create_user_update, admin_users_delete

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', admins_users, name='admins_users'),
    path('users_create/', admin_users_create, name='admin_users_create'),
    path('users_update/<int:id>/', create_user_update, name='create_user_update'),
    path('admin_users_delete/<int:id>/', admin_users_delete, name='admin_users_delete'),
]

