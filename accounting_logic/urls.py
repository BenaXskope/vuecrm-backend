from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/create_category/', views.api_create_category),
    path('api/get_categories/', views.api_get_categories),
    path('api/edit_category/', views.api_edit_category),
    path('api/get_category_by_id/', views.api_get_category_by_id),
    path('api/create_record/', views.api_create_record),
    path('api/get_all_records/', views.api_get_all_records),
    path('api/get_record_by_id/', views.api_get_record_by_id)
]
