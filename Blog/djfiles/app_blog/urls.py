from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', BlogListView.as_view(), name='main'),
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('create_post/', PostCreateFormView.as_view(), name='create_post'),
    path('account/', account, name='account'),
    path('upload_blog/', update_blog, name='upload_blog')

]