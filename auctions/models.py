from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
#python3 manage.py makemigrations
#python3 manage.py migrate
class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.categoryName}"

class Listing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    startingBid = models.FloatField(default=0)
    imageUrl = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="categories", blank=True)
    description = models.TextField(max_length=1000, blank=True)
    activeStatus = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listing")
    bidAmount = models.FloatField(default=0)
    def __str__(self):
        return f"{self.user} bided ${self.bidAmount} for {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    commentContent = models.TextField(max_length=1000)
    def __str__(self):
        return f"{self.user} commented {self.commentContent} on {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_listing")
    class Meta:
        unique_together = ["user", "listing"]
    def __str__(self):
        return f"{self.user} added {self.listing} to his/her watchlist"
