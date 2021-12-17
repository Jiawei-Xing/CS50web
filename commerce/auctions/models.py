from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    
    
class Listing(models.Model):
    CATEGORIES = [
        ('food','food'),
        ('clothes','clothes'),
        ('tools', 'tools'),
        ('others', 'others'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owners")
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=64)
    starting = models.IntegerField()
    price = models.IntegerField(null=True)
    image = models.CharField(max_length=256, blank=True)
    category = models.CharField(max_length=7, choices=CATEGORIES)
    watchers = models.ManyToManyField(User, blank=True, related_name="watch_listings")
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} from {self.owner} with ${self.price}. #{self.category}"

       
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_listings")
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    
    def __str__(self):
        return f"{self.bidder} offered ${self.bid} on {self.listing.title}"
    
    
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listings")
    comment = models.CharField(max_length=256)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
    time = models.TimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f"{self.commenter} commented '{self.comment}' on {self.listing.title}"

