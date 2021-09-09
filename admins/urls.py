from django.urls import path

from admins.views import index, UserListView, UserCreateView, UserUpdateView, UserDeleteView

app_name = 'admins'

urlpatterns = [
    path('', index, name='index'),
    path('users/', UserListView.as_view(), name='admins_users'),
    path('users_create/', UserCreateView.as_view(), name='admin_users_create'),
    path('users_update/<int:pk>/', UserUpdateView.as_view(), name='create_user_update'),
    path('admin_users_delete/<int:pk>/', UserDeleteView.as_view(), name='admin_users_delete'),
]

