from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("<int:status>/listings", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:category_id>/categories", views.categories, name="categories"),
    path("<int:listing_id>/view", views.view_listing, name="view_listing"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/close", views.close, name="close"),
]
