from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.utils import timezone
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Category, Auction, Bid, Comment
from .forms import MakeBid, AddComment, EditAuction, CreateNew


def index(request):
    active = Auction.objects.filter(active=True).all()
    return render(request, "auctions/index.html", {
        'active': active
    })

def listing(request, title):
    listing = Auction.objects.get(title=title)
    if not listing:
        return HttpResponseRedirect(reverse('index'))

    if timezone.now() >= listing.expires:
        listing.active = False
        listing.save()

    count = Bid.objects.filter(listing=listing).count()
    comments = Comment.objects.filter(listing=listing).all().order_by('-id')

    form = MakeBid()
    commentForm = AddComment()
    return render(request, "auctions/listing.html", {
        'listing': listing,
        'count': count,
        'comments': comments,
        'form': form,
        'commentForm': commentForm
    })
        

@login_required
def AddBid(request, title):
    listing = Auction.objects.get(title=title)
    if not listing:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = MakeBid(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["amount"]
            try:
                b = Bid.objects.create(
                    user=request.user,
                    listing=listing,
                    bid=bid
                )
                b.save()
                print("Saved Bid")
            except:
                print("Error, unable to save comment")
    return redirect('listing', title)


@login_required
def CommentAdd(request, title):
    listing = Auction.objects.get(title=title)
    if not listing:
        return HttpResponseRedirect(reverse('index'))

    if request.method == "POST":
        form = AddComment(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            try:
                c = Comment.objects.create(
                    user=request.user,
                    listing=listing,
                    comment=comment
                )
                c.save()
                print("Saved Comment")
            except:
                print("Error, unable to save comment")
    return redirect('listing', title)

@login_required
def edit_list(request, title):
    listing = Auction.objects.get(title=title)
    if not listing:
        print("No Listing")
        return HttpResponseRedirect(reverse('index'))
            
    if request.user != listing.user:
        print("Doesnt match")
        return redirect('listing', title)

    bids = Bid.objects.filter(listing=listing).all()
    highest_bid = Bid.objects.filter(listing=listing).all().aggregate(Max('bid'))
    form = EditAuction(initial={
        'title': listing.title,
        'desc': listing.desc,
        'active': listing.active,
        'expires': listing.expires
    })


    if request.method == "POST":
        form = EditAuction(request.POST, request.FILES)  
        if form.is_valid():
            t = form.cleaned_data["title"]
            desc = form.cleaned_data["desc"]
            active = form.cleaned_data["active"]
            expires = form.cleaned_data["expires"]
            img = request.FILES["img"]

            if t != title:
                if Auction.objects.get(title=t):
                    return render(request, "auctions/edit.html", {
                        'listing': listing,
                        'bids': bids,
                        'highest_bid': highest_bid,
                        'form': form,
                        'message': 'Title is not unique'
                    })
            
            if timezone.now() >= expires:
                return render(request, "auctions/edit.html", {
                    'listing': listing,
                    'bids': bids,
                    'highest_bid': highest_bid,
                    'form': form,
                    'message': 'Expiration Date is set to past'
                })

            listing.title = t
            listing.desc = desc
            listing.active = active
            listing.expires = expires
            listing.img = img
            listing.save()
                   

        return redirect('listing', title)
        
    return render(request, "auctions/edit.html", {
        'listing': listing,
        'bids': bids,
        'highest_bid': highest_bid,
        'form': form
    })

def categories(request):
    cate = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'cate': cate
    })

def list_cate(request, cate):
    c = Auction.objects.filter(category=cate).all()
    if not c:
        return redirect('index')

    return render(request, "auctions/list_category.html", {
        'items': c
    })

@login_required
def new(request):
    if request.method == "POST":
        form = CreateNew(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["desc"]
            active = form.cleaned_data["active"]
            expires = form.cleaned_data["expires"]
            category = form.cleaned_data["category"]
            price = form.cleaned_data["price"]
            img = request.FILES["img"]

            if Auction.objects.filter(title=title):
                return render(request, "auctions/new.html", {
                    'form': form,
                    'message': 'Title Already Exists'
                })

            if timezone.now() > expires:
                return render(request, "auctions/new.html", {
                    'form': form,
                    'message': 'Expiration Date is set in the past'
                })

            try:
                new = Auction.objects.create(
                    user=request.user,
                    title=title,
                    desc=desc,
                    category=category,
                    price=price,
                    active=active,
                    expires=expires,
                    img=img
                )
                new.save()
                print("Hello")
            except:
                print("Unable to Save")
                return render(request, "auctions/new.html", {
                    'form': form,
                    'message': 'Unable to save new listing'
                })

            return redirect('listing', title)

        return render(request, "auctions/new.html", {
            'form': form,
            'message': 'Form Not Valid'
        })

    form = CreateNew()
    return render(request, "auctions/new.html", {
        'form': form
    })


# Authentication System

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


@login_required
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
