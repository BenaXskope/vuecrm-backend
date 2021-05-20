from django.db import models as models
from django.contrib.auth.models import User
from django.db.models import *

# Create your models here.


class Category(models.Model):
    user = ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE,
                         related_name="categories")
    title = TextField(verbose_name="Название")
    limit = DecimalField(verbose_name="Лимит", max_digits=20, decimal_places=2, blank=False)


class Record(models.Model):
    user = ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE,
                      related_name="records")
    category = ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE,
                          related_name="records")
    amount = DecimalField(verbose_name="Сумма", max_digits=20, decimal_places=2, blank=False)
    description = TextField(verbose_name="Описание")
    date = DateTimeField(verbose_name="Дата")
    type = TextField(verbose_name="Тип", default='income')
