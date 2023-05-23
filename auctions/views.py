from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from datetime import datetime

from .models import User, Category, Listing, Comment, Bid


def index(request):
    active_listings = Listing.objects.filter(status=True).order_by("-created_on")
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
    })
    
    
def closed_listings(request):
    closed_listings = Listing.objects.filter(status=False).order_by("-created_on")
    return render(request, "auctions/closed_listings.html", {
        "closed_listings": closed_listings,
    })    


def product_page(request, product_id):
    product = Listing.objects.get(pk=product_id)
    comments = Comment.objects.filter(listing=product)
    isinwatchlist = request.user in product.watchers.all()

    is_seller = False
    if request.user.username == product.seller.username:
        is_seller = True
    
    return render(request, "auctions/product_page.html", {"product": product, "isinwatchlist": isinwatchlist, "comments": comments, "bid_msg": "no_bid", "is_seller": is_seller, "message": None})


def category_items(request, category_type):
    category= Category.objects.get(category_type=category_type)
    listings = Listing.objects.filter(status=True, category=category)
    return render(request, "auctions/category_items.html", {
        "listings": listings, "category": category,
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


def categories(request):
    all_categories = Category.objects.all()
    
    return render(request, "auctions/categories.html", {
        "categories": all_categories,
    })
    

@login_required(login_url="/login")
def place_bid(request, product_id):
    placed_bid = request.POST['bid']
    product = Listing.objects.get(pk=product_id)
    comments = Comment.objects.filter(listing=product)
    isinwatchlist = request.user in product.watchers.all()

    is_seller = False
    if request.user.username == product.seller.username:
        is_seller = True
    
    if not placed_bid:
        return render(request, "auctions/product_page.html", {"product": product, "isinwatchlist": isinwatchlist, "comments": comments, "bid_msg": "low_bid", "is_seller": is_seller, "message": None})
        
    
    if (float(placed_bid) > product.start_bid.bid_amount):
        new_bid = Bid(user=request.user, bid_amount=placed_bid)
        new_bid.save()
        product.start_bid = new_bid
        product.save()
        return render(request, "auctions/product_page.html", {"product": product, "isinwatchlist": isinwatchlist, "comments": comments, "bid_msg": "high_bid", "is_seller": is_seller, "message": None})
    else:
        return render(request, "auctions/product_page.html", {"product": product, "isinwatchlist": isinwatchlist, "comments": comments, "bid_msg": "low_bid", "is_seller": is_seller, "message": None})


@login_required(login_url="/login")
def add_comment(request, product_id):
    writer = request.user
    listing = Listing.objects.get(pk=product_id)
    comment = request.POST['comment']
    
    add_comment = Comment(writer = writer, listing = listing, comment_msg = comment)
    add_comment.save()
    
    return HttpResponseRedirect(reverse("product_page", args=(product_id, )))


@login_required(login_url="/login")
def watchlist(request):
    user = request.user
    products = Listing.objects.filter(watchers = user.id).order_by("-created_on")
    return render(request, "auctions/watchlist.html", {
        "products": products, 
    })
    
    
@login_required(login_url="/login")
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        category = request.POST["category"]
        start_bid = request.POST["starting_bid"]
        image_url = request.POST["image_url"]
        
        current_datetime = datetime.now()
        current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")
        
        current_bid = Bid(user = request.user, bid_amount = float(start_bid))
        current_bid.save()
        
        user = request.user
        category_value = Category.objects.get(category_type = category)
        
        new_product = Listing(title = title, description = description, category = category_value, start_bid = current_bid, image_url = image_url, seller = user, status = True, created_on = current_datetime)
        
        new_product.save()
        
        return HttpResponseRedirect(reverse("index",))
        
    categories = Category.objects.all()
    return render(request, "auctions/create_listing.html", {
        "categories": categories,
    })
    
    
@login_required(login_url="/login")
def watch_add(request, product_id):
    listing_details = Listing.objects.get(pk=product_id)
    user = request.user
    listing_details.watchers.add(user)
    return HttpResponseRedirect(reverse("product_page", args=(product_id, )))


@login_required(login_url="/login")
def watch_remove(request, product_id):
    listing_details = Listing.objects.get(pk=product_id)
    user = request.user
    listing_details.watchers.remove(user)
    return HttpResponseRedirect(reverse("product_page", args=(product_id, )))    
    
    
@login_required(login_url="\login")
def close_auction(request, product_id):
    product = Listing.objects.get(pk = product_id)
    product.status = False
    product.save()
    isinwatchlist = request.user in product.watchers.all()
    comments = Comment.objects.filter(listing=product)

    is_seller = False
    if request.user.username == product.seller.username:
        is_seller = True
    
    return render(request, "auctions/product_page.html", {"product": product, "isinwatchlist": isinwatchlist, "comments": comments, "bid_msg": None, "is_seller": is_seller, "message": "closed"})
    