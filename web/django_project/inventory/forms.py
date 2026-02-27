from django import forms
from .models import Product, Customer, Order, OrderItem
from django.core.exceptions import ValidationError

from core.models.customer import Customer as CoreCustomer
from core.models.product import Product as CoreProduct
from core.exceptions.base import InvalidEmailException, InvalidQuantityException, OutOfStockException


class ProductForm(forms.ModelForm):
    # Define category choices (you can expand this list as needed)
    CATEGORIES = [
        ('', '-- Select Category --'),

        ('Electronics', 'Electronics'),
        ('Computers & Laptops', 'Computers & Laptops'),
        ('Mobile Phones & Tablets', 'Mobile Phones & Tablets'),
        ('Networking Equipment', 'Networking Equipment'),

        ('Office Furniture', 'Office Furniture'),
        ('Home Furniture', 'Home Furniture'),
        ('Furniture', 'Furniture'),
        ('Storage & Cabinets', 'Storage & Cabinets'),

        ('Office Supplies', 'Office Supplies'),
        ('Stationery', 'Stationery'),
        ('Printing & Scanning', 'Printing & Scanning'),

        ('Computer Accessories', 'Computer Accessories'),
        ('Mobile Accessories', 'Mobile Accessories'),
        ('Audio & Video Accessories', 'Audio & Video Accessories'),

        ('Tools & Equipment', 'Tools & Equipment'),
        ('Cleaning Supplies', 'Cleaning Supplies'),
        ('Safety Equipment', 'Safety Equipment'),
        ('Others', 'Others'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        error_messages={
            'required': "Please select a category."
        }
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity_in_stock']

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        qty = cleaned_data.get('quantity_in_stock')
        name = cleaned_data.get('name')
        category = cleaned_data.get('category')

        if price is not None and qty is not None:
            try:
                CoreProduct(None, name, category, float(price), qty)
            except (ValueError, InvalidQuantityException) as e:
                raise ValidationError(str(e))

        return cleaned_data


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']

    def clean_email(self):
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        try:
            CoreCustomer(id=None, name=name, email=email)
        except InvalidEmailException as error:
            raise ValidationError(str(error))
        return email


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']
        error_messages = {
            'customer': {
                'required': "Please select a customer."
            }
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']
        error_messages = {
            'product': {
                'required': "Please select a product."
            }
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        product = self.cleaned_data.get('product')

        if product and qty:
            core_prod = CoreProduct(
                id=product.id,
                name=product.name,
                category=product.category,
                price=product.price,
                quantity_in_stock=product.quantity_in_stock
            )
            try:
                core_prod.remove_stock(qty)
            except (OutOfStockException, InvalidQuantityException) as e:
                raise ValidationError(str(e))
            
        return qty


