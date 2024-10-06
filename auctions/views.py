from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(active=True) # Passing a variable with all active listings to the view
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def add_listing(request):
    if request.method == "POST":
        userId_local = request.user
        title_local = request.POST["title"]
        description_local = request.POST["description"]
        startBid_local = request.POST["startBid"]
        imageUrl_local = request.POST["imageUrl"]
        category_local = Category.objects.get(category=request.POST["category"])

        # Checks if the listing already exists and prevents duplicate values after page refresh after adding a new listing
        if Listing.objects.filter(title = title_local) or Listing.objects.filter(description = description_local):
            return render(request, "auctions/addlisting.html", {
                "categories": Category.objects.all(),
                "message" : "There is already a listing like this one!"
            })
        else:
            # Add a new listing
            newListing = Listing(userId=userId_local, title=title_local, description=description_local, startBid=startBid_local, imageUrl=imageUrl_local, category=category_local)
            newListing.save()

            return render(request, "auctions/addlisting.html", {
                "categories": Category.objects.all(),
                "message" : "Listing created successfully!"
            })
    else:
        # It loads a blank addlisting page if the method is not POST, if it's not loaded by a form call
        return render(request, "auctions/addlisting.html", {
        "categories": Category.objects.all()
        })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    # Using the relative_name bids on the Bid model used to reference the Listing model and retrieve it's bids
    if listing.bids.last() is not None:
        return render(request, "auctions/listing.html",{
            "listing": listing,
            "lastBid": listing.bids.last().bid
        })
    else:
        return render(request, "auctions/listing.html",{
            "listing": listing
        })

def bid(request, listing_id):
    if request.method == "POST":
        userId_local = request.user
        listing_local = Listing.objects.get(pk = listing_id)
        bid_local = request.POST["bid"]
        startBid = listing_local.startBid
        lastBidTrue = listing_local.bids.last()
               

        def renderMessage(listingObj, message):
            if lastBidTrue is not None:
                return render(request, "auctions/listing.html", {
                    "listing" : listingObj,
                    "message" : message,
                    "lastBid" : listingObj.bids.last().bid
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing" : listingObj,
                    "message" : message
                })
        
        if lastBidTrue is not None:
            lastBidValue = lastBidTrue.bid
            if float(bid_local) <= float(lastBidValue):
                return renderMessage(listing_local, f"Your bid must be higher than U${lastBidValue}")
            else:
                newBid = Bid(userId=userId_local, listingId = listing_local, bid = bid_local)
                newBid.save()
                return renderMessage(listing_local, "New bid given!")
        else:
            if float(bid_local) <= startBid:
                return renderMessage(listing_local, f"Your bid must be higher than U${startBid}")
            else:
                newBid = Bid(userId=userId_local, listingId = listing_local, bid = bid_local)
                newBid.save()
                return renderMessage(listing_local, "New bid given!")
    else:
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))