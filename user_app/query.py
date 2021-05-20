from datetime import datetime
from django.db.models import Q, Count, Avg
from django.contrib.auth.models import User
from .models import Profile


def create_user(data):
    email = data['email']
    username = email
    password = data['password']
    name = data['name']
    user = User.objects.create_user(username=username, email=email, password=password)
    profile = Profile(user=user, name=name)
    user.save()
    profile.save()
    return {
        'user': {
            'email': user.email,
            'name': profile.name,
            'bill': profile.bill,
            'locale': profile.locale
        },
    }


def update_profile(user, data):
    profile = Profile.objects.get(user=user)
    profile.name = data['name']
    profile.bill = data['bill']
    profile.locale = data['locale']
    profile.save()
    return {
        'name': profile.name,
        'bill': profile.bill,
        'locale': profile.locale
    }
