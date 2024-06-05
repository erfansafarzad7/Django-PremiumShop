from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='item_category')
    price = models.PositiveSmallIntegerField()
    discount = models.PositiveSmallIntegerField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        return int(self.price * (1 - self.discount / 100))
