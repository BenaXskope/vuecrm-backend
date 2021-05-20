from django.db import models as models
from django.contrib.auth.models import User
from django.db.models import *
import binascii
import os
import uuid
# Create your models here.


class Value(models.Model):
    value = TextField("Значение")

    class Meta:
        verbose_name = 'Значение'
        verbose_name_plural = 'Значения'

    def __str__(self):
        return self.value


class Profile(models.Model):
    name = TextField(verbose_name='Имя', blank=True)
    user = OneToOneField(User, unique=True, verbose_name="Пользователь", on_delete=models.CASCADE,
                         related_name="profile")
    bill = DecimalField("Рублей", max_digits=20, default=0, decimal_places=2)
    locale = TextField(verbose_name='Язык', default='ru-RU')

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class BrowserData(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_agent_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='HTTP_USER_AGENT', blank=True, null=True, related_name='agents')
    http_accept_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='HTTP_ACCEPT', blank=True, null=True, related_name='accepts')
    accept_lang_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='HTTP_ACCEPT_LANGUAGE', blank=True, null=True, related_name='langs')
    accept_encoding_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='HTTP_ACCEPT_ENCODING', blank=True, null=True, related_name='encodings')
    x_forwarded_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='HTTP_X_FORWARDED_FOR', blank=True, null=True, related_name='forwards')
    remote_addr_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='REMOTE_ADDR', blank=True, null=True, related_name='remotes')
    guid_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='GUID', blank=True, null=True, related_name='guids')
    luid_val = ForeignKey('user_app.Value', on_delete=models.CASCADE, verbose_name='LUID', blank=True, null=True, related_name='luids')


    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Данные браузера'
        verbose_name_plural = 'Данные браузера'

    def __str__(self):
        return '%s' % self.pk


class Token(models.Model):
    key = CharField(verbose_name="Ключ", max_length=40, primary_key=True)
    user = ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE, verbose_name="Пользователь")
    is_active = BooleanField(verbose_name="Активен", default=True)
    created_at = DateTimeField(verbose_name="Создан", auto_now_add=True)

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return "{} {}".format(self.key, self.user)