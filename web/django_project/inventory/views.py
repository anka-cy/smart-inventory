from django.shortcuts import render, redirect
from django.http import Http404
from mysql.connector import Error as MySQLError
from django.contrib import messages
from .models import Product, Customer, Order, OrderItem
from django.forms import inlineformset_factory
from .forms import ProductForm, CustomerForm, OrderForm, OrderItemForm

from core.services.analytics_service import *

from database.dao.customer_dao import CustomerDAO
from database.dao.product_dao import ProductDAO
from database.dao.order_dao import OrderDAO

from core.models.customer import Customer as CoreCustomer
from core.models.product import Product as CoreProduct
from core.models.order import Order as CoreOrder


def dashboard(request):

    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    context = {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': get_total_revenue(),
        'best_sellers': get_best_selling_products(),
        'stock_value': get_stock_value(),
        'avg_order_value': get_avg_order_value(),
        'monthly_revenue': get_monthly_revenue(),
        'customer_stats': get_customer_frequency()
    }

    return render(request, 'inventory/dashboard.html', context)


def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


def product_create(request):
    title = 'Add Product'
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_product = CoreProduct(
                id=None,
                name=data['name'],
                category=data['category'],
                price=float(data['price']),
                quantity_in_stock=data['quantity_in_stock']
            )

            ProductDAO().save(new_product)

            messages.success(request, 'Product added successfully')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'inventory/product_form.html', {'form': form, 'title': title})


def product_update(request, pk):
    title = 'Edit Product'

    core_product = ProductDAO().find_by_id(pk)
    if not core_product:
        raise Http404("Product not found in our database.")

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            updated_product = CoreProduct(
                id=pk,
                name=data['name'],
                category=data['category'],
                price=float(data['price']),
                quantity_in_stock=data['quantity_in_stock']
            )
            ProductDAO().update(updated_product)
            messages.success(request, 'Product details updated')
            return redirect('product_list')
    else:
        # Pre-fill form using 'initial' data from our Core object
        form = ProductForm(initial={
            'name': core_product.name,
            'category': core_product.category,
            'price': core_product.price,
            'quantity_in_stock': core_product.quantity_in_stock
        })
    return render(request, 'inventory/product_form.html', {'form': form, 'title': title})


def product_delete(request, pk):
    core_product = ProductDAO().find_by_id(pk)
    if not core_product:
        raise Http404("Product not found.")

    if request.method == 'POST':
        try:
            ProductDAO().delete(pk)
            messages.success(request, 'Product deleted successfully')
            return redirect('product_list')
        except MySQLError:
            messages.error(request, "Cannot delete this product because there's an active order.")
            return redirect('product_list')

    return render(request, 'inventory/product_confirm_delete.html', {'product': core_product})


def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_customer = CoreCustomer(
                id=None,
                name=data['name'],
                email=data['email']
            )
            CustomerDAO().save(new_customer)
            messages.success(request, 'New customer registered')
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'inventory/customer_form.html', {'form': form})


def order_list(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'inventory/order_list.html', {'orders': orders})


def order_detail(request, pk):
    order = OrderDAO().find_by_id(pk)
    if not order:
        raise Http404("Order not found.")
    
    return render(request, 'inventory/order_detail.html', {'order': order})


def order_create(request):
    OrderItemFormSet = inlineformset_factory(
        Order, OrderItem, form=OrderItemForm,
        extra=0, min_num=1,can_delete=True
    )

    if request.method == 'POST':
        form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            try:
                cust = form.cleaned_data['customer']
                core_customer = CoreCustomer(cust.id, cust.name, cust.email)
                core_order = CoreOrder(id=None, customer=core_customer)

                for item_form in formset.forms:
                    if not item_form.cleaned_data:
                        continue
                    p = item_form.cleaned_data['product']
                    qty = item_form.cleaned_data['quantity']
                    
                    core_product = CoreProduct(p.id, p.name, p.category, float(p.price), p.quantity_in_stock)
                    core_order.add_item(core_product, qty)
                    core_product.remove_stock(qty)


                OrderDAO().save(core_order)
                messages.success(request, 'Order placed successfully')
                return redirect('order_list')

            except Exception as e:
                messages.error(request, str(e))

    else:
        form = OrderForm()
        formset = OrderItemFormSet()

    return render(request, 'inventory/order_form.html', {'form': form, 'formset': formset})
