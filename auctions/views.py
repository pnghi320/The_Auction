from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Listing,Category,Bid,Comment,Watchlist
from django.db.models import Max
from django.urls import reverse

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()})

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


def listing (request, listing_id):
    currentlListing = Listing.objects.get(id=listing_id)
    #comments = Comment.objects.filter(listing = currentlListing)
    #listing_ids = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)
    comment_ids = Comment.objects.filter(listing = currentlListing).values_list('id', flat=True)
    if currentlListing.activeStatus:
        return render(request, "auctions/listing.html", {
        "comments": Comment.objects.filter(pk__in=comment_ids),
        "listing": currentlListing})
    else:
        winningBidAmount = Bid.objects.filter(listing = currentlListing).aggregate(Max('bidAmount'))
        winningBid = winningBidAmount.get("bidAmount__max", "")
        if winningBid:
            winner = Bid.objects.get(bidAmount=winningBid, listing=currentlListing).user
            print(winningBidAmount)
            print(winningBid)
            print(winner)
            return render(request, "auctions/listing.html", {
            "winner": winner,
            "comments": Comment.objects.filter(pk__in=comment_ids),
            "listing": currentlListing})
        else:
            return render(request, "auctions/listing.html", {
            "comments": Comment.objects.filter(pk__in=comment_ids),
            "listing": currentlListing})


def createListing (request):
    if request.method == "POST":
        # Attempt to create new user
        try:
            listingTitle = request.POST.get("title")
            listingStartingBid = request.POST.get("startingBid")
            if listingStartingBid == '': 
                listingStartingBid = 0
            if listingTitle == '':
                listingTitle = "No Title"
            category_id = request.POST.get('category')
            usedCategory = Category.objects.get(pk = category_id)
            listing = Listing(user = request.user, title=listingTitle, imageUrl=request.POST.get("url"), category = usedCategory,startingBid = listingStartingBid, description = request.POST.get("description"))
            listing.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/createListing.html",{
            "categories": Category.objects.all()
            })

def watchlist(request, listing_id):
    if request.user.is_authenticated:
        try:
            watchlistItem = Watchlist(user = request.user, listing = Listing.objects.get(id=listing_id))
            watchlistItem.save()
        except IntegrityError:
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    
def watchlistRemove(request, listing_id):
    if request.user.is_authenticated:
        try:
            removedWatchlist = Watchlist.objects.filter(user = request.user, listing = Listing.objects.get(id=listing_id))
            removedWatchlist.delete()
        except IntegrityError:
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))   
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

def userWatchlist(request):
    listing_ids = Watchlist.objects.filter(user=request.user).values_list('listing', flat=True)
    return render(request, "auctions/userWatchlist.html", {
        "listings": Listing.objects.filter(pk__in=listing_ids)})

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()})

def categorizedListings (request, category_id):
    currentCategory = Category.objects.filter(id=category_id)
    categoryName = currentCategory[0].categoryName
    return render(request, "auctions/categorizedListings.html", {
        "listings": Listing.objects.filter(category__in=currentCategory),
        "category": categoryName})

def createBid (request, listing_id):
    if request.POST.get('userBid') == "":
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    if request.method == "POST":
        currentlListing = Listing.objects.get(id=listing_id)
        userBid = request.POST.get('userBid')
        Listing.objects.filter(pk=listing_id).update(startingBid=userBid)
        bid = Bid(user = request.user, listing=currentlListing, bidAmount=userBid)
        bid.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))

def closeListing (request, listing_id):
    Listing.objects.filter(pk=listing_id).update(activeStatus=False)
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))

def comment (request, listing_id):
    if request.POST.get('comment') == "":
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))
    if request.method == "POST":
        currentlListing = Listing.objects.get(id=listing_id)
        newcomment = request.POST.get('comment')
        comment = Comment(user = request.user, listing=currentlListing, commentContent=newcomment)
        comment.save()
        return HttpResponseRedirect(reverse('listing', args=[listing_id]))