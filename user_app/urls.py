from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/token_auth/', views.MyObtainAuthToken.as_view()),
    path('api/check_auth/', views.api_check_auth),
    path('api/logout/', views.api_logout),
    path('api/register/', views.api_register),
    path('api/get_profile_info/', views.api_my_profile),
    path('api/update_profile/', views.api_update_profile)
]
