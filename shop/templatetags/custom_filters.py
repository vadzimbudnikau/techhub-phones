from django import template

register = template.Library()


@register.filter
def calculate_total_price(item):
    return item.product.price * item.quantity
