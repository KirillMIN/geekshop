from django.db import models
from users.models import User
from products.models import Product
# Create your models here.


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_times = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username, } продукт {self.product.name}'
