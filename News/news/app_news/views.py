
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from app_news.models import Comments, News, Category
from app_news.forms import NewsForm, CommentsForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


class NewsCreateFormView(PermissionRequiredMixin,LoginRequiredMixin,View):
    """страница создания новости"""
    permission_required = ('app_news.add_news')

    def get(self, request):
        news_form = NewsForm()
        return render(request, 'app_news/news.html', context={'news_form': news_form})

    def post(self, request):
        news_form = NewsForm(request.POST)
        if news_form.is_valid():
            News.objects.create(**news_form.cleaned_data)
            return HttpResponseRedirect('/')
        return render(request, 'app_news/news.html', context={'news_form': news_form})

class NewsEditFormView(PermissionRequiredMixin,LoginRequiredMixin,View):
    """страница редактирования новости"""
    permission_required = ('app_news.change_news')


    def get(self, request, profile_id):
        news = News.objects.get(id=profile_id)
        news_form = NewsForm(instance=news)
        return render(request, 'app_news/edit.html', context={'news_form': news_form,
                                                              'profile_id': profile_id})

    def post(self, request, profile_id):
        news = News.objects.get(id=profile_id)
        news_form = NewsForm(request.POST, instance=news)

        if news_form.is_valid():
            news.save()
            return HttpResponseRedirect(reverse('news_list'))
        return render(request, 'app_news/edit.html', context={'news_form': news_form,
                                                              'profile_id': profile_id})


class AllNewsListView(ListView):
    """список всех новостей, упорядоченный по дате и активности"""
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.filter()
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return News.objects.filter(is_active='A').order_by('create_date')


class AllNewsDetailView(DetailView):
    """детальная страница выбранной новости и комментарии к ним"""
    model = News
    pk_url = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comments.objects.filter(user_news=self.get_object())

        return context

# def show_comment(request, pk:int): #старая страница комментариев к новостям
#     comment = Comments.objects.filter(user_news=pk)
#     return render(request, 'app_news/com.html', {'comment': comment})

# class CommentsListView(ListView):
#     model = Comments
#     template_name = 'comments_list.html'
#     context_object_name = 'comments_list'
#     queryset = Comments.objects.filter(user_news=1)

class CommentCreateFormView(View):
    """Добавление комментария к новости"""
    def get(self, request, pk):
        comment_form = CommentsForm(is_authenticated=self.request.user.is_authenticated)
        return render(request, 'app_news/create_comment.html', context={'comment_form': comment_form})

    def post(self, request, pk):
        comment_form = CommentsForm(request.POST, is_authenticated=self.request.user.is_authenticated)
        if comment_form.is_valid():
            if self.request.user.is_active:
                comment_form.cleaned_data['user_name'] = self.request.user
                comment_form.cleaned_data['user'] = self.request.user
                comment_form.cleaned_data['user_news_id'] = pk
            else:
                comment_form.cleaned_data['user_news_id'] = pk
            Comments.objects.create(**comment_form.cleaned_data)
            return HttpResponseRedirect(reverse('news_detail', kwargs={'pk':pk}))
        return render(request, 'app_news/create_comment.html', context={'comment_form': comment_form})


def show_category(request, cat_id):
    """функция фильтра по категориям на главной страницу"""
    news = News.objects.filter(cat_id=cat_id).order_by('create_date')
    cats = Category.objects.all()
    context = {
        'cats': cats,
        'news_list': news,
        'cat_selected': cat_id
    }
    return render(request, 'app_news/news_list.html', context=context)