from django.db import models
from authorization.models import Users
from authorization.models import User_adresses
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # avatar = models.ImageField(upload_to='avatars/', blank=True)
    address = models.ForeignKey(User_adresses, on_delete=models.SET_NULL,
    null=True, # разрешаем NULL в БД
    blank=True)
    about = models.CharField(max_length=128, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    # vk = models.CharField(max_length=100, blank=True)
    # Все дополнительные поля здесь