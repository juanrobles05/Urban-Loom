from django.db import models
# from accounts.models import User
# from catalog.models import Product

# Create your models here.
# class ProductRecommendation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="recommended_to")
#     reason = models.CharField(max_length=255, blank=True, help_text="Ej: Basado en compras previas")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Recomendación: {self.product.name} para {self.user.email}"
