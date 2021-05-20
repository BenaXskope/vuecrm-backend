from datetime import datetime
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from accounting_logic.models import Category, Record


def get_categories(user):
    categories = Category.objects.filter(user=user)
    return categories


def get_category_by_id(user, data):
    category = Category.objects.filter(user=user).get(pk=data['id'])
    return category


def create_category(user, data):
    category = Category(user=user, title=data['title'], limit=data['limit'])
    category.save()
    return category


def edit_category(user,  data):
    category = Category.objects.filter(user=user).get(pk=int(data['id']))
    category.title = data['title']
    category.limit = data['limit']
    category.save()
    return category


def get_all_records(user):
    records = Record.objects.filter(user=user)
    return records


def get_category_records(user, data):
    records = Record.objects.filter(user=user).filter(category__pk=data['category_id'])
    return records


def get_record_by_id(user, data):
    record = Record.objects.filter(user=user).get(pk=int(data['id']))
    return record


def create_record(user, data):
    category = Category.objects.filter(user=user).get(pk=data['categoryId'])
    record = Record(user=user, category=category, amount=data['amount'], description=data['description'], type=data['type'],
                    date=data['date'])
    record.save()
    return record
