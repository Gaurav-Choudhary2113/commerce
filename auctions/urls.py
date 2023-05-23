from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category_type>", views.category_items, name="category_items"),
    path("listing/<int:product_id>", views.product_page, name="product_page"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("remove/<int:product_id>", views.watch_remove, name="watch_remove"),
    path("add/<int:product_id>", views.watch_add, name="watch_add"),
    path("add_comment/<int:product_id>", views.add_comment, name="add_comment"),
    path("place_bid/<int:product_id>", views.place_bid, name="place_bid"),
    path("close_auction/<int:product_id>", views.close_auction, name="close_auction"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    
]
