from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("uploadNote", views.upload_file, name="uploadNote"),
    path("profile/<int:id>", views.profile, name=" profile"),
    path("filter/", views.filters, name="filter"),
    path("search", views.searchs, name="search"),
    path("uploadEvent", views.upload_event, name="uploadEvent"),
    path("event", views.event, name="event")

]
