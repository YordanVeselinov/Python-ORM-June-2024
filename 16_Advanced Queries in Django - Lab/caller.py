import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import Product, Category, Customer, Order, OrderProduct
from django.db.models import Sum, Q, F


# Create and run queries
def product_quantity_ordered() -> str:
    result = []

    products = Product.objects.annotate(
        total_quantity=Sum('orderproduct__quantity')
    ).filter(total_quantity__gt=0).order_by('-total_quantity')

    for product in products:
        result.append(f'Quantity ordered of {product.name}: {product.total_quantity}')

    return '\n'.join(result)


def ordered_products_per_customer() -> str:
    result = []
    orders = Order.objects.prefetch_related('orderproduct_set__product__category')

    for order in orders:
        result.append(f'Order ID: {order.id}, Customer: {order.customer.username}')
        for product_order in order.orderproduct_set.all():
            result.append(f'- Product: {product_order.product.name}, Category: {product_order.product.category.name}')

    return '\n'.join(result)


def filter_products() -> str:
    result = []

    products = Product.objects.filter(
        Q(is_available=True) &
        Q(price__gt=3.00)
    ).order_by('-price', 'name')

    for product in products:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)


def give_discount() -> str:
    result = []

    Product.objects.filter(
        Q(is_available=True) &
        Q(price__gt=3.00)
    ).update(price=F('price') * 0.70)

    products = Product.objects.filter(is_available=True).order_by('-price', 'name')

    for product in products:
        result.append(f'{product.name}: {product.price}lv.')

    return '\n'.join(result)
