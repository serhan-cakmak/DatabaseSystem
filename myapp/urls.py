from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("dashboard", views.dashboard, name="dashboard"),
    path("add", views.add, name="add"),
    path("add_player", views.add_player, name="add_player"),
    path("add_coach", views.add_coach, name="add_coach"),
    path("add_jury", views.add_jury, name="add_jury"),
    path("update_stadium", views.update, name="update"),
    path("delete_session", views.delete_session, name="delete_session"),
    path("list_stadiums", views.list_stadiums, name="list_stadiums"),
    path("add_match", views.add_match, name="add_match"),
    path("get_info", views.get_info, name="get_info"),
    path("rate", views.rate, name="rate"),
    path("add_squad", views.add_squad, name="add_squad"),
]