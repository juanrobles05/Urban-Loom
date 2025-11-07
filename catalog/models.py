from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Collection(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('LIMITED', 'Limited'),
        ('SOLD OUT', 'Sold Out'),
        ('ARCHIVE', 'Archive'),
    ]

    name = models.CharField(max_length=100, unique=True)
    season = models.CharField(max_length=10, help_text="e.g., FW24, SS24")
    description = models.TextField()
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    is_current = models.BooleanField(default=False, help_text="Mark as current featured collection")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.season}"

    def get_status_color(self):
        """Return Tailwind CSS class for status color"""
        status_colors = {
            'AVAILABLE': 'bg-green-500',
            'LIMITED': 'bg-yellow-500',
            'SOLD OUT': 'bg-red-500',
            'ARCHIVE': 'bg-gray-500',
        }
        return status_colors.get(self.status, 'bg-gray-500')

    @property
    def pieces(self):
        """Compute pieces automatically from related products (count of products)."""
        return self.products.count()


class Category(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('limited', 'Limited'),
        ('archive', 'Archive'),
        ('sold_out', 'Sold Out'),
    ]

    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name

    @property
    def pieces(self):
        """Compute pieces automatically from related products (count of products)."""
        return self.products.count()


class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="El precio debe ser mayor que cero")]
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Validación personalizada del modelo"""
        super().clean()
        if self.price is not None and self.price < 0:
            raise ValidationError({'price': 'El precio no puede ser negativo'})
    
    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones solo en precio"""
        # Solo validar si estamos actualizando o si es un save desde formulario
        validate = kwargs.pop('validate', True)
        if validate:
            # Validar solo el precio
            if self.price is not None and self.price < 0:
                raise ValidationError({'price': 'El precio no puede ser negativo'})
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name