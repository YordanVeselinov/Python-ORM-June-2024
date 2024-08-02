import os
import django



from main_app.populate_db import populate_model_with_data

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Profile, Order, Product
from django.db.models import Q, Count, F, Value, Case, When, BooleanField

# Import your models here

# Create queries within functions
def get_profiles(search_string=None) -> str:
    if search_string is None:
        return ''

    profiles = Profile.objects.filter(
        Q(full_name__icontains=search_string)
        |
        Q(email__icontains=search_string)
        |
        Q(phone_number__icontains=search_string)
    ).order_by('full_name')

    if not profiles.exists():
        return ''

    result = []

    for p in profiles:
        result.append(f'Profile: {p.full_name}, '
                      f'email: {p.email}, '
                      f'phone number: {p.phone_number}, '
                      f'orders: {p.orders.count()}')

    return '\n'.join(result)


def get_loyal_profiles() -> str:
    profiles = Profile.objects.get_regular_customers()

    if not profiles.exists():
        return ''

    result = []

    for p in profiles:
        result.append(f'Profile: {p.full_name}, orders: {p.order_count}')

    return '\n'.join(result)


def get_last_sold_products() -> str:
    last_order = Order.objects.prefetch_related('products').last()

    if not last_order or not last_order.products:
        return ''

    products = ', '.join([p.name for p in last_order.products.order_by('name')])

    return f'Last sold products: {products}'


def get_top_products() -> str:
    top_products = Product.objects.annotate(
        order_count=Count('orders'),
    ).filter(order_count__gt=0).order_by('-order_count', 'name')[:5]

    if not top_products.exists():
        return ''

    result = ['Top products:']

    for p in top_products:
        result.append(f'{p.name}, sold {p.order_count} times')

    return '\n'.join(result)


def apply_discounts() -> str:
    orders_to_apply = Order.objects.annotate(
        products_count=Count('products'),
    ).filter(is_completed=False, products_count__gt=2).update(total_price=F('total_price') * 0.90)

    return f'Discount applied to {orders_to_apply} orders.'


def complete_order() -> str:
    order = Order.objects.filter(
        is_completed=False
    ).order_by(
        'creation_date'
    ).first()

    if not order:
        return ""

    order.products.update(
        in_stock=F('in_stock') - 1,
        is_available=Case(
            When(in_stock=1, then=Value(False)),
            default=F('is_available'),
            output_field=BooleanField()
        )
    )

    order.is_completed = True
    order.save()

    return "Order has been completed!"
