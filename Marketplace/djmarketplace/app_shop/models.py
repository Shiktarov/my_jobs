from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='Название Магазина')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'магаз'
        verbose_name_plural = 'магазины'

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                       args=[self.slug])

class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Название товара')
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.CharField(max_length=2000, verbose_name='Описание')
    image = models.ImageField(upload_to='media/', blank=True, null=True, verbose_name='image')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='остаток на складе')
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='привязка к магазу')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail',
                       args=[self.id, self.slug])
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'






