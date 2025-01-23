from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LogInView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]