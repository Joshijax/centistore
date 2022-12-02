from django import template
from core.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def getDiscountPrice(item):
    val = int(item.price) + int(item.discount_price)
    return val


@register.filter
def getDiscountPer(item):

    val = int(item.price) + int(item.discount_price)
    val1 = (int(item.discount_price) / val) * 100
    return int(val1)
