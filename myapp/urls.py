from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("player", views.player, name="player"),
    path("admin", views.admin, name="admin"),
    path("coach", views.coach, name="match"),
]