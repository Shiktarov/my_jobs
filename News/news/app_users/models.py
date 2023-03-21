from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    city = models.CharField(max_length=36, blank=True)
    date_of_birth =models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=False)
    sale_card = models.IntegerField(null=True, blank=False)
