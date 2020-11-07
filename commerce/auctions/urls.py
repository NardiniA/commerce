from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:cate>", views.list_cate, name = "list_cate"),
    path("listings/<str:title>", views.listing, name="listing"),
    path("listings/<str:title>/edit", views.edit_list, name = "edit"),
    path("new", views.new, name="new"),
    path("profile", views.profile, name="profile"),
    path("listings/<str:title>/addComment", views.CommentAdd, name="addcomment"),
    path("listings/<str:title>/makeBid", views.AddBid, name="makebid")
]
