from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path("home",  views.home, name="home"),
    path("cinema", views.cinema, name="cinema"),
    path("book", views.book, name="book"),
    path("travel", views.travel, name="travel"),
    path("food", views.food, name="food"),
    path("profile/<username>",views.profile, name="profile"),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path("new_post/", views.new_post, name="new_post"),

] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)