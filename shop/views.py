from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
)
from django.db.models import Sum, Q
from .models import Product, Cart, Order, UserProfile
from .forms import UserProfileForm


class HomeView(TemplateView):
    """View for the home page."""

    template_name = "shop/home.html"


class ProductCatalogView(ListView):
    """View to display the product catalog."""

    model = Product
    template_name = "shop/product_catalog.html"
    context_object_name = "products"
    paginate_by = 6
    ordering = "price"

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filtering by query
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(description__icontains=query.lower())
            )

        # Filtering by price range
        price_range = self.request.GET.get("price_range")
        if price_range:
            min_price, max_price = map(int, price_range.split("-"))
            queryset = queryset.filter(price__gte=min_price, price__lte=max_price)

        # Filtering by manufacturer
        manufacturer = self.request.GET.get("manufacturer")
        if manufacturer and manufacturer != "all":
            queryset = queryset.filter(manufacturer=manufacturer)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_manufacturer"] = self.request.GET.get("manufacturer", "all")
        context["selected_price_range"] = self.request.GET.get(
            "price_range", "0-1000000"
        )
        context["manufacturers"] = Product.objects.values_list(
            "manufacturer", flat=True
        ).distinct()
        return context


class ProductDetailView(DetailView):
    """View to display the details of a specific product."""

    model = Product
    template_name = "shop/product_detail.html"


class AddToCartView(View):
    """View to add a product to the user's cart."""

    def post(self, request, product_id):
        """Handles the HTTP POST method to add a product to the cart."""
        if request.user.is_authenticated:  # Проверяем, авторизован ли пользователь
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = Cart.objects.get_or_create(
                user=request.user, product=product
            )

            if not created:
                cart_item.order = Cart.objects.filter(user=request.user).count() + 1
                cart_item.save()

            cart_item.quantity += 1
            cart_item.save()

            # Update the cart count in session
            cart_counts = Cart.objects.filter(user=request.user).aggregate(
                total_quantity=Sum("quantity")
            )
            cart_count = cart_counts["total_quantity"] or 0
            request.session["cart_count"] = cart_count

            return redirect("shop:product_detail", pk=product_id)
        else:
            # Handle case when user is not authenticated
            # You can redirect to a login page or show an error message
            return redirect(
                "shop:login"
            )  # Redirect to login page, change to your actual login URL


class CheckoutView(LoginRequiredMixin, View):
    """View for the checkout process."""

    def get(self, request):
        """Handles the HTTP GET method to display the cart and total price."""
        user_cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in user_cart)
        return render(
            request,
            "shop/checkout.html",
            {"user_cart": user_cart, "total_price": total_price},
        )

    def post(self, request):
        """Handles the HTTP POST method for placing an order."""
        user_cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in user_cart)

        order = Order.objects.create(user=request.user, total_price=total_price)
        order.products.set([item.product for item in user_cart])
        user_cart.delete()

        # Update the cart count in session
        cart_count = Cart.objects.filter(user=request.user).count()
        request.session["cart_count"] = cart_count

        return redirect("shop:order_detail", pk=order.pk)


class OrderDetailView(LoginRequiredMixin, View):
    """View to display the details of a specific order."""

    def get(self, request, pk):
        """Handles the HTTP GET method to display the details of an order."""
        order = Order.objects.filter(user=request.user, pk=pk).first()
        return render(request, "shop/order_detail.html", {"order": order})


class CartView(LoginRequiredMixin, View):
    """View to display the user's cart."""

    def get(self, request):
        """Handles the HTTP GET method to display the user's cart."""
        user_cart = Cart.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in user_cart)

        # Update the cart count in session
        cart_count = Cart.objects.filter(user=request.user).count()
        request.session["cart_count"] = cart_count

        return render(
            request,
            "shop/cart.html",
            {"user_cart": user_cart, "total_price": total_price},
        )


class CartRemoveView(View):
    """View to remove a product from the cart."""

    @method_decorator(require_POST)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handles the HTTP POST method to remove a product from the cart."""
        product_id = self.kwargs["product_id"]
        cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
        cart_item.delete()

        # Update the cart count in session
        cart_count = (
            Cart.objects.filter(user=request.user).aggregate(Sum("quantity"))[
                "quantity__sum"
            ]
            or 0
        )
        request.session["cart_count"] = cart_count

        return redirect("shop:cart")


class UserOrderListView(LoginRequiredMixin, View):
    """View to display the list of orders for the logged-in user."""

    def get(self, request):
        """Handles the HTTP GET method to display the list of orders."""
        user_orders = Order.objects.filter(user=request.user).order_by("-created_at")
        return render(request, "shop/user_orders.html", {"user_orders": user_orders})


class RegisterView(CreateView):
    """View for user registration."""

    form_class = UserCreationForm
    template_name = "shop/register.html"
    success_url = reverse_lazy("shop:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class UserLoginView(LoginView):
    """View for user login."""

    template_name = "shop/login.html"
    success_url = reverse_lazy("shop:home")


class UserLogoutView(LogoutView):
    """View for user logout."""

    next_page = reverse_lazy("shop:home")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View to update user profile information."""

    model = UserProfile
    form_class = UserProfileForm
    template_name = "shop/profile_update.html"
    success_url = reverse_lazy("shop:profile_detail")

    def get_object(self, queryset=None):
        user_profile, created = UserProfile.objects.get_or_create(
            user=self.request.user
        )
        return user_profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """View to display user profile information."""

    model = UserProfile
    template_name = "shop/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user.userprofile


@login_required
def delete_profile(request):
    """View to delete user profile and related data."""
    user_profile = request.user.userprofile

    with transaction.atomic():
        # Delete related data if exists
        if hasattr(user_profile.user, "orders"):
            user_profile.user.orders.all().delete()
        if hasattr(user_profile.user, "cart"):
            user_profile.user.cart.all().delete()

        user_profile.user.delete()

    return redirect("shop:home")


def page_not_found(request, exception):
    """View function to handle 404 (page not found) errors."""

    return render(request, "shop/404.html", status=404)
