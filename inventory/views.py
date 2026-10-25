from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order



from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render
from .models import Product


def dashboard(request):
    total_products = Product.objects.count()

    total_units = Product.objects.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    stock_value = Product.objects.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("price") * F("quantity"),
                output_field=DecimalField(
                    max_digits=12,
                    decimal_places=2
                )
            )
        )
    )["total"] or 0

    low_stock_products = Product.objects.filter(
        quantity__lte=5
    ).order_by("quantity", "name")

    context = {
        "total_products": total_products,
        "total_units": total_units,
        "stock_value": stock_value,
        "low_stock_products": low_stock_products,
        "low_stock_count": low_stock_products.count(),
    }

    return render(request, "dashboard.html", context)


def product_list(request):
    products = Product.objects.all().order_by('name')
    return render(request, 'product_list.html',
                  {'products': products})


def add_product(request):
    if request.method == 'POST':
        Product.objects.create(
            name=request.POST['name'],
            category=request.POST['category'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            description=request.POST.get('description', '')
        )
        return redirect('product_list')

    return render(request, 'product_form.html')


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.name = request.POST['name']
        product.category = request.POST['category']
        product.price = request.POST['price']
        product.quantity = request.POST['quantity']
        product.description = request.POST.get('description', '')
        product.save()
        return redirect('product_list')

    return render(request, 'product_form.html',
                  {'product': product})


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(request, 'delete_product.html',
                  {'product': product})


def order_list(request):
    orders = Order.objects.select_related('product').all()
    return render(request, 'order_list.html',
                  {'orders': orders})


def add_order(request):
    products = Product.objects.filter(quantity__gt=0)

    if request.method == 'POST':
        customer = request.POST['customer_name']
        product = get_object_or_404(
            Product, pk=request.POST['product']
        )
        quantity = int(request.POST['quantity'])

        if quantity > 0 and quantity <= product.quantity:
            Order.objects.create(
                customer_name=customer,
                product=product,
                quantity=quantity
            )
            product.quantity -= quantity
            product.save()
            return redirect('order_list')

        return render(request, 'order_form.html', {
            'products': products,
            'error': 'Enter a valid quantity within available stock.'
        })

    return render(request, 'order_form.html',
                  {'products': products})
