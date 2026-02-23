from django import forms
from .models import Product, Customer, Order, OrderItem
from django.core.exceptions import ValidationError

from core.models.customer import Customer as CoreCustomer
from core.models.product import Product as CoreProduct
from core.exceptions.base import InvalidEmailException, OutOfStockException, InvalidQuantityException


class ProductForm(forms.ModelForm):
    # Define category choices (you can expand this list as needed)
    CATEGORIES = [
        ('', '-- Select Category --'),

        ('electronics', 'Electronics'),
        ('computers', 'Computers & Laptops'),
        ('mobile_devices', 'Mobile Phones & Tablets'),
        ('networking', 'Networking Equipment'),

        ('office_furniture', 'Office Furniture'),
        ('home_furniture', 'Home Furniture'),
        ('storage', 'Storage & Cabinets'),

        ('office_supplies', 'Office Supplies'),
        ('stationery', 'Stationery'),
        ('printing', 'Printing & Scanning'),

        ('computer_accessories', 'Computer Accessories'),
        ('mobile_accessories', 'Mobile Accessories'),
        ('audio_video', 'Audio & Video Accessories'),

        ('tools', 'Tools & Equipment'),
        ('cleaning', 'Cleaning Supplies'),
        ('safety', 'Safety Equipment'),
        ('others', 'Others'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORIES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'quantity_in_stock']

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        qty = cleaned_data.get('quantity_in_stock')
        name = cleaned_data.get('name', '')
        category = cleaned_data.get('category', '')

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


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

    def clean(self):
        cleaned_data = super().clean()
        product_obj = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity')

        if product_obj and quantity:
            try:
                core_p = CoreProduct(
                    id=product_obj.id,
                    name=product_obj.name,
                    category=product_obj.category,
                    price=float(product_obj.price),
                    quantity_in_stock=product_obj.quantity_in_stock
                )
                core_p.remove_stock(quantity)
            except (OutOfStockException, InvalidQuantityException) as e:
                raise ValidationError(str(e))

        return cleaned_data
