from django.db import models
from django.contrib.auth.hashers import make_password, check_password



def user_avatar_path(instance, filename):
    return f'avatars/user_{instance.id}/{filename}'

class Users(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name="Email адрес",
        help_text="Введите действующий email"
    )
    password = models.CharField(max_length=128)

    # avatar = models.ImageField(
    #     upload_to=user_avatar_path,
    #     default='avatars/default_avatar.jpg',
    #     blank=True,
    #     null=True,
    #     verbose_name="Аватар"
    # )

    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.name


class User_adresses(models.Model):
    user = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="Пользователь"
    )
    ADDRESS_TYPES = [
        ('home', 'Домашний'),
        ('work', 'Рабочий'),
        ('other', 'Другой'),
    ]
    address_type = models.CharField(
        max_length=20,
        choices=ADDRESS_TYPES,
        default='home',
        verbose_name="Тип адреса"
    )

    is_default = models.BooleanField(
        default=False,
        verbose_name="Основной адрес"
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город"
    )

    street = models.CharField(
        max_length=200,
        verbose_name="Улица"
    )

    house = models.CharField(
        max_length=20,
        verbose_name="Дом"
    )

    apartment = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Квартира/офис"
    )
    # подъезд
    entrance = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Подъезд"
    )
    floor = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Этаж"
    )
    intercom = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Домофон"
    )
    comment = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(auto_now_add=True)
