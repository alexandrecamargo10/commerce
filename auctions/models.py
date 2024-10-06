from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.CASCADE, related_name="listings")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    startBid = models.DecimalField(max_digits=9, decimal_places=2)
    imageUrl = models.URLField(max_length=200, blank=True)
    category = models.ForeignKey(Category, null=True, on_delete = models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.CASCADE, related_name="bids")
    listingId = models.ForeignKey(Listing, null=True, on_delete = models.CASCADE, related_name="bids")
    bid =  models.DecimalField(max_digits=9, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Listing: {self.listingId.id} User: {self.userId} U$ {self.bid} {self.date}"

class Comment(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete = models.CASCADE, related_name="comments")
    listingId = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.pk}"

