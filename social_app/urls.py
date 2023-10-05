from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("", views.home, name="home"),
    path('admin/', admin.site.urls),         
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('social-auth/', include('social_django.urls', namespace="social")), # handles OAuth calls
    path('dashboard', views.dashboard, name="dashboard"),
]