from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment, Watchlist
from .forms import ListingForm, BidForm, CommentForm


# Redirect to index page
def home(request):
    return HttpResponseRedirect(reverse("index", args=[1]))


# display either active listings or closed listings
def index(request, status):
    # Check to see if the status is active
    if status == 1:
        listings = Listing.objects.filter(is_active=True).order_by('title')
        is_active = True
    else:
        listings = Listing.objects.filter(is_active=False).order_by('title')
        is_active = False

    # Update the price for the listings
    for listing in listings:
        if Bid.objects.filter(listing=listing):
            price = Bid.objects.filter(listing=listing).last()
            listing.starting_price = price.amount
        else:
            pass

    return render(request, "auctions/index.html", {
        "listings": listings,
        "is_active": is_active
    })


# Log user in
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index", args=[1]))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", args=[1]))


# Register user
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", args=[1]))
    else:
        return render(request, "auctions/register.html")


# Create new listing
@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid:
            listing = form.save(commit=False)
            listing.owner = User.objects.get(id=request.user.id)
            listing.is_active = "True"
            listing.save()
            return HttpResponseRedirect(reverse("index", args=[1]))
    return render(request, "auctions/create_listing.html", {
        "form": ListingForm()
    })


# Control categores on the website
def categories(request, category_id):
    # Display the list of categories
    if category_id == 0:
        categories = Category.objects.all()
        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    else:
        listings = Listing.objects.filter(category=category_id)
        category = Category.objects.get(id=category_id)
        return render(request, "auctions/category_list.html", {
            "listings": listings,
            "category": category
        })


# Display listing to user
def view_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    try:
        user = User.objects.get(id=request.user.id)
        # Check to see if the user can close their listing
        if listing.owner == user:
            closing = True
        else:
            closing = None
    except ObjectDoesNotExist:
        user = None
        closing = None
    # update the price to the highest bid
    if Bid.objects.filter(listing=listing):
        price = Bid.objects.filter(listing=listing).last()
        listing.starting_price = price.amount
    if Comment.objects.all():
        # Sort comments by when they were created
        comments = Comment.objects.filter(listing=listing, ).order_by('-id')

    # If closed Find the highest bidder
    if listing.is_active is True:
        winner = 1
    elif listing.is_active is False:
        try:
            highest_bid = Bid.objects.filter(listing=listing).last()
        except ObjectDoesNotExist:
            highest_bid = None
        if highest_bid is None:
            winner = 0
            pass
        elif highest_bid.bidder == user:
            winner = 2
        elif highest_bid.bidder != user:
            winner = 0

    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "bid": BidForm(),
        "comment": CommentForm(),
        "comments": comments,
        "closing": closing,
        "winner": winner,
    })


# Define a watchlist
@login_required
def watchlist(request, listing_id):
    # Display a user with his list of watchlist items
    if listing_id == 0:
        watcher = User.objects.get(id=request.user.id)
        try:
            listings = Watchlist.objects.get(watcher=watcher)
            alllistings = Listing.objects.filter(watchlists=listings)
        except ObjectDoesNotExist:
            alllistings = None
        return render(request, "auctions/watchlist.html", {
            "listings": alllistings
        })

    # Get the current listing
    listing = Listing.objects.get(id=listing_id)

    # Check if the user already has a watchlist
    try:
        watcher = User.objects.get(id=request.user.id)
        watch_item = Watchlist.objects.get(watcher=watcher)
        alllistings = Listing.objects.filter(watchlists=watch_item)

        # add the first item back to an empty list
        if not alllistings:
            watch_item.listing.add(listing)

        # If the user is already watching the item delete it
        for item in alllistings:
            if item == listing:
                watch_item.listing.remove(listing)
            else:
                # Add to user watchlist
                watch_item.listing.add(listing)

    except ObjectDoesNotExist:
        watch_item = None

    # Start a new watchlist for the user
    if watch_item is None:
        watch_item = Watchlist(watcher=watcher)
        watch_item.save()
        watch_item.listing.add(listing)
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))


# Define the bid function
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid:
            bid_item = form.save(commit=False)
            listing = Listing.objects.get(id=listing_id)

            # Make sure the listing is active
            if listing.is_active is False:
                return render(request, "auctions/error_page.html", {
                    "message": "Sorry, this listing is already closed."
                })

            # Make sure the bid is not on the same person's item
            if listing.owner == User.objects.get(id=request.user.id):
                return render(request, "auctions/error_page.html", {
                    "message": "Sorry, you may not bid on your own item."
                    })

            # Check if the item as any bids
            try:
                prior_bid = Bid.objects.filter(listing=listing).last()
            except ObjectDoesNotExist:
                prior_bid = None

            # Make sure the bid is high enough
            if prior_bid is None:
                if listing.starting_price >= bid_item.amount:
                    return render(request, "auctions/error_page.html", {
                        "message": "Sorry, your bid is too low."
                        })
                else:
                    bid_item.listing = listing
                    bidder = User.objects.get(id=request.user.id)
                    bid_item.bidder = bidder
                    bid_item.save()
                    return HttpResponseRedirect(reverse("view_listing", args=[listing.id]))

            # If other bids exist check to make current bid is higher than starting price and other bids
            if listing.starting_price >= prior_bid.amount or prior_bid.amount >= bid_item.amount:
                return render(request, "auctions/error_page.html", {
                    "message": "Sorry, your bid is too low."
                    })
            else:
                bid_item.listing = listing
                bidder = User.objects.get(id=request.user.id)
                bid_item.bidder = bidder
                bid_item.save()
                return HttpResponseRedirect(reverse("view_listing", args=[listing.id]))


# Allow commenting functionality
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.listing = Listing.objects.get(id=listing_id)
            comment.commenter = User.objects.get(id=request.user.id)
            comment.save()
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))


# close the Bid if the user is the owner
@login_required
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.is_active = False
    listing.save()
    return HttpResponseRedirect(reverse("view_listing", args=[listing_id]))
