from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.name}"


class Listing(models.Model):
    title = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings_b", blank=True, null=True)
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.title}: {self.description} (${self.starting_price}) Active: {self.is_active}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids_l")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_b")
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"{self.bidder} bid (${self.amount}) for {self.listing}"



class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_c")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments_l")
    body = models.TextField()
    created_on = models.TimeField(auto_now=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing.title}"


class Watchlist(models.Model):
    watcher = models.OneToOneField(User, on_delete=models.CASCADE, related_name="watchlists_w")
    listing = models.ManyToManyField(Listing, blank=True, related_name="watchlists")

    def __str__(self):
        return f"{self.watcher}'s watchlist"