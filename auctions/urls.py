from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("createListing", views.createListing, name="createListing"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("watchlistRemove/<int:listing_id>", views.watchlistRemove, name="watchlistRemove"),
    path("userWatchlist", views.userWatchlist, name="userWatchlist"),
    path("categories", views.categories, name="categories"),
    path("categorizedListings/<int:category_id>", views.categorizedListings, name="categorizedListings"),
    path("createBid/<int:listing_id>", views.createBid, name="createBid"),
    path("closeListing/<int:listing_id>", views.closeListing, name="closeListing"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
