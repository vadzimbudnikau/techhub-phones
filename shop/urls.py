from django.urls import path
from . import views

app_name = "shop"

handler404 = "shop.views.page_not_found"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path(
        "product-catalog/", views.ProductCatalogView.as_view(), name="product_catalog"
    ),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path(
        "add-to-cart/<int:product_id>/",
        views.AddToCartView.as_view(),
        name="add_to_cart",
    ),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("order/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path(
        "cart/remove/<int:product_id>/",
        views.CartRemoveView.as_view(),
        name="cart_remove",
    ),
    path("user-orders/", views.UserOrderListView.as_view(), name="user_orders"),
    path("accounts/profile/", views.ProfileDetailView.as_view(), name="profile_detail"),
    path(
        "accounts/profile/update",
        views.UserProfileUpdateView.as_view(),
        name="profile_update",
    ),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("accounts/profile/delete/", views.delete_profile, name="profile_delete"),
]
