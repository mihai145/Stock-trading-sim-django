from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("stock", views.stock_search, name="stock_search"),
    path("stock/<str:symbol>", views.stock_view, name="stock_view"),
    path("profile", views.profile_view, name="profile"),
    path("invest", views.invest, name="invest"),
    path("buy/<str:symbol>", views.buy, name="buy"),
    path("sell/<str:symbol>", views.sell, name="sell")
]
