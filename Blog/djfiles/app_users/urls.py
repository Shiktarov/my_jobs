from django.urls import path
from app_users.views import AnotherLoginView, another_register_view, AnotherLogoutView, edit_account


urlpatterns = [
    path('another_login/', AnotherLoginView.as_view(), name='another_login'),
    path('logout/', AnotherLogoutView.as_view(), name='logout'),
    path('register/', another_register_view, name='register'),
    path('account/edit/', edit_account, name='edit_profile')

]