from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.NewList, name="NewList"),
    path("morInfomations/<int:id>/", views.Informations, name="morInfomations"),
    path("displaycategory", views.displaycategory, name="displaycategory"),
    path("addWatchlist/<int:id>/", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:id>/", views.removeWatchlist, name="removeWatchlist"),
    path("MyWatchilist", views.Watchilist, name="watchilist"),
    path("newBid/<int:id>/",views.newBid,name="newBid"),
    path("SaveComment/<int:id>",views.SaveComment,name="SaveComment")


    
]
