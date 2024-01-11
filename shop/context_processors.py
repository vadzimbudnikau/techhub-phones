from django.db.models import Sum
from .models import Cart


def cart_count(request):
    """
    Helper function to calculate the total quantity of items in the user's cart.

    Args:
        request (HttpRequest): The request object passed to the view.

    Returns:
        dict: A dictionary containing the calculated cart count.
    """
    if request.user.is_authenticated:
        cart_count = (
            Cart.objects.filter(user=request.user).aggregate(Sum("quantity"))[
                "quantity__sum"
            ]
            or 0
        )
        return {"cart_count": cart_count}
    return {"cart_count": 0}
