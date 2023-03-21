from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Post(models.Model):
    title = models.CharField(max_length=200, default='Запись', blank=True,  verbose_name=_('title'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name=_('author'))
    body = models.TextField(verbose_name=_('description'))
    create_date = models.DateTimeField(verbose_name=_('created date'), default=timezone.now)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = _('posts')
        verbose_name = _('post')


class Images(models.Model):
    post = models.ForeignKey(Post, null=True, blank=True, related_name='image_blog_post', on_delete=models.CASCADE, verbose_name=_('images'))
    image = models.ImageField(upload_to='files/', blank=True, null=True, verbose_name=_('image file'))

    class Meta:
        verbose_name_plural = _('images')
        verbose_name = _('image')