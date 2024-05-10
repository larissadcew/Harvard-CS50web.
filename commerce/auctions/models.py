from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    categoryname = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryname

class Bid(models.Model):
    bid_user = models.ManyToManyField(User)
    bid = models.IntegerField(default=0)

    def __str__(self):
        return f" the User: {self.bid_user},The Bid{self.bid}"
  
class Listing(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    url = models.CharField(max_length=200,blank=True)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE , related_name="category")
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Listing,on_delete=models.CASCADE,null=True)


class Comments(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    listing = models.ForeignKey(Listing , on_delete=models.CASCADE,blank=True,null=True)
    comments = models.CharField(max_length=200)

    