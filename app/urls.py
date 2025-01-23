from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.view_file, name='view_file'),
    path('change_privacy/<int:file_id>/', views.change_privacy, name='change_privacy'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
]