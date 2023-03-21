from django.urls import path
from . import views
from .views import *
urlpatterns = [
    path('all_news/news_form/', NewsCreateFormView.as_view(), name='create_news'),
    path('all_news/', AllNewsListView.as_view(), name='news_list'),
    path('news_list/<int:pk>', AllNewsDetailView.as_view(), name="news_detail"),
    path('news_list/<int:profile_id>/edit', NewsEditFormView.as_view(), name='edit_news'),
    # path('news_list/<int:pk>/comments', CommentsListView.as_view() ),
    #path('news_list/<int:pk>/comments', views.show_comment, name='view_comment'),
    path('news_list/<int:pk>/comment_form/', CommentCreateFormView.as_view(), name='create_comment'),
    path('category/<int:cat_id>/', show_category, name='category')
]
