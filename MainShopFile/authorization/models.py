from django.db import models
from django.contrib.auth.hashers import make_password, check_password

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


