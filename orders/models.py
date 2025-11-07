from django.db import models
from accounts.models import User
from catalog.models import Product

# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Carrito de {self.user.email}"

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def get_total_price(self):
        return sum(item.get_total() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en carrito de {self.cart.user.email}"

    def get_total(self):
        return self.quantity * self.product.price


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pendiente"),
        ("paid", "Pagada"),
        ("shipped", "Enviada"),
        ("completed", "Completada"),
        ("cancelled", "Cancelada"),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ("card", "Tarjeta de Crédito/Débito"),
        ("check", "Cheque Bancario"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.ForeignKey(
        "accounts.ShippingAddress", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"Orden {self.id} - {self.user.email}"
    
    def calculate_total(self):
        """Calcula el total de la orden basado en los items"""
        return sum(item.get_total() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"