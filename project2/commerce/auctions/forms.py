from django import forms
from .models import User, Category, Listing, Bid, Comment, Watchlist

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_price", "image", "category"]


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["body"]