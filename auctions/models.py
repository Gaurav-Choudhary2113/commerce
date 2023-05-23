from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass
    
    def __str__(self) -> str:
        return f"{self.username}"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_type = models.CharField(max_length=127)
    
    def __str__(self) -> str:
        return f"{self.category_type}"   

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bid")
    bid_amount = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.bid_amount}"
    

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    start_bid = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name="bid_price")
    image_url = models.URLField(null=True, blank=True)
    status = models.BooleanField(default=True)          # True if the listing is active
    created_on = models.CharField(null=True, max_length=16)
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_products")
    
    def __str__(self):
        return f"{self.title}: {self.description}\n {self.category} , {self.image_url}, {'active' if self.status else 'inactive'}. {self.created_on} by {self.seller}. Watched by: {self.watchers}\n"


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="product")
    comment_msg = models.TextField(max_length=200)
    
    def __str__(self):
        return f"Comment on {self.listing}: {self.comment_msg} by {self.writer}"
