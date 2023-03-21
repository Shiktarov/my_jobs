from _csv import reader

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Post, Images
from app_blog.forms import PostForm, UploadPostsForm, MultiFileForm
from django.views.generic import ListView, DetailView


def account(request):
    '''страница инфо профиля'''
    user = request.user
    return render(request, 'app_users/account.html', {'user': user})


class BlogListView(ListView):
    model = Post
    template_name = 'app_blog/main.html'

    def get_queryset(self):
        return Post.objects.order_by('-create_date')

class BlogDetailView(DetailView): # новое
    model = Post
    template_name = 'app_blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = Images.objects.filter(post=self.get_object())

        return context



class PostCreateFormView(LoginRequiredMixin,View):
    """страница создания записи"""

    def get(self, request):
        post_form = PostForm()
        image_form = MultiFileForm()
        return render(request, 'app_blog/create_post.html', context={'post_form': post_form,
                                                                     'image_form': image_form})

    def post(self, request):
        post_form = PostForm(request.POST, request.FILES)
        image_form = MultiFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if post_form.is_valid():
            post_form.cleaned_data['author'] = self.request.user
            new_blog_post = Post.objects.create(**post_form.cleaned_data)
            new_blog_post.save()
            if image_form.is_valid():
                for f in files:
                    new_image = Images.objects.create(**image_form.cleaned_data)
                    new_image.image = f
                    new_image.post = new_blog_post
                    new_image.save()
            return HttpResponseRedirect('/')
        return render(request, 'app_blog/create_post.html', context={'post_form': post_form,
                                                                     'image_form': image_form})

def update_blog(request):
    if request.method == 'POST':
        upload_file_form = UploadPostsForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            blog_file = upload_file_form.cleaned_data['file'].read()
            blog_str = blog_file.decode('utf-8').split('\n')
            csv_reader = reader(blog_str, delimiter=',', quotechar='"')
            for row in csv_reader:
                Post.objects.create(create_date=(row[0]), body=(row[1]), author=request.user)
            return HttpResponseRedirect(reverse('main'))
    else:
        upload_file_form = UploadPostsForm()

    context = {
        'form': upload_file_form
    }
    return render(request, 'app_blog/upload_post.html', context=context)