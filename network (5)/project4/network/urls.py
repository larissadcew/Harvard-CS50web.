
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newPost"),
    path('perfil/<int:id>', views.get_perfil, name="perfil"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('follow/', views.follow, name="follow"),
    path('Following/', views.Following, name="Following"),
    path('Edit/<int:id>', views.Edit, name="Edit"),
    path("addLike/<int:id>", views.add_like, name="addLike"),
    path("removeLike/<int:id>", views.remove_like, name="removeLike"),

]
