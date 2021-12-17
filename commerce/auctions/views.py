from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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
        

@login_required        
def create(request):
    if request.method == "POST":
    
        # error check
        if request.POST['title'] == '' or request.POST['text'] == '' or request.POST['bid'] == '':
            return HttpResponse("Error: missing information! Must provide title, description and starting bid.")
        
        else:
            # create new listing
            Listing.objects.create(owner=request.user, title=request.POST['title'], text=request.POST['text'], 
                starting=request.POST['bid'], image=request.POST['image'], category=request.POST['category'])
            return HttpResponseRedirect(reverse("index"))
    else:
        categories = ['clothes', 'food', 'tools', 'others']
        return render(request, "auctions/create.html", {"categories": categories})
        
       
def listing_page(request, listing_id, message=''):
    listing = Listing.objects.get(pk=listing_id)
    
    # submit via POST
    if request.method == "POST":
    
        # not logged in
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('login'))
    
        # bid by user
        if listing.status and "bid" in request.POST:
            bid = int(request.POST['bid'])
            
            # check bid validation
            if (listing.price == None and bid >= listing.starting) or bid > listing.price:
                Bid.objects.create(bidder=request.user, bid=bid, listing=listing)
                listing.price = bid
                listing.save()
                message = "Successful bid!"
            else:
                message = "Invalid bid! Must be larger than current price."
        
        # watchlist by user
        elif "watchlist" in request.POST:
        
            # remove user from watchlist
            if request.user in listing.watchers.all():
                listing.watchers.remove(request.user)
                message = "Removed from watchlist! "

            # add user to watchlist
            else:
                listing.watchers.add(request.user)
                message = "Added to watchlist! "
        
        # close listing by owner
        elif request.user == listing.owner and "close" in request.POST:
            listing.status = False
            listing.save()
            
        # comment by user
        elif "comment" in request.POST:
            Comment.objects.create(commenter=request.user, comment=request.POST['comment'], listing=listing)

    # closed listing    
    if not listing.status:
        message += "This listing has been closed. "
                    
        # inform the winner user
        bid = Bid.objects.filter(listing=listing).last()
        if bid:
            if request.user == bid.bidder:
                message += "You are the winner!"
            
    return render(request, "auctions/listing.html", {
        "listing": listing, "message": message, "user": request.user, "comments": Comment.objects.filter(listing=listing)
    })
    
    
@login_required
def watchlist(request):
    listings = request.user.watch_listings.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


def categories(request):
    categories = ['clothes', 'food', 'tools', 'others']
    return render(request, "auctions/categories.html", {
        "categories" : categories
    })
    
    
def category_list(request, category):
    listings = Listing.objects.filter(category=category, status=True)
    return render(request, "auctions/category_list.html", {
        "category": category, "listings": listings
    })
    
    
    
