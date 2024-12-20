from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('', views.home, name='home'),
    path('change_privacy/<int:file_id>/', views.change_privacy, name='change_privacy'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]

