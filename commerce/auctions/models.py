from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"

# Dynamic Categories
choices = Category.objects.all().values_list('name', 'name')

# Category List
categories = []

# Adds all categories from db
for item in choices:
    categories.append(item)

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True)
    desc = models.CharField(max_length=500)
    img = models.ImageField()
    category = models.CharField(max_length=50, choices=categories)
    price = models.FloatField(default=50.00)
    active = models.BooleanField(default=True)
    expires = models.DateTimeField(null=False)

    def __str__(self):
        return f"{self.title}"

    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ""
        return url


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f"{self.user} - {self.listing} - {self.bid}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=False)

    def __str__(self):
        return f"{self.user}'s Comment for {self.listing}"
