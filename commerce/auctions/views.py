from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.urls import reverse


from .models import User,Listing,Bid,Category,Watchlist,Comments



def index(request):
    listing = Listing.objects.filter(isActive=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listing":listing,
        "categories":categories
         
    })
 
def displaycategory(request):
    if request.method == 'POST':
        category_name = request.POST['category']
        
        category = Category.objects.get(categoryname=category_name)

        activeListing = Listing.objects.filter(isActive=True, category=category)

        all_category = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listing": activeListing,
            "categories": all_category
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


def NewList(request):
    if request.method == 'GET':
        
        # get category
        category = Category.objects.all()

        return render(request,"auctions/newlisting.html",{
            "categories":category
        })
    else:
        # Getting form data
        title = request.POST['title']
        description = request.POST['description']
        initial_price = request.POST['price']
        url = request.POST['url']
        category_name = request.POST['category']

        # Current user
        current_user = request.user

        new_bid = Bid.objects.create(bid_user=current_user, bid=initial_price)


        # Retrieving category
        try:
            category = Category.objects.get(categoryname=category_name)
        except Category.DoesNotExist:
            # Handle case where category doesn't exist
            return HttpResponse("Category does not exist.")

        # Creating a new listing
        new_listing = Listing.objects.create(
            author=current_user,
            title=title,
            price=new_bid,
            description=description,
            url=url,
            category=category
        )

        # Save the new listing
        new_listing.save()

        # Redirect or render a success message
        return HttpResponseRedirect(reverse(index))


    
def Informations(request,id):
    if request.method == "GET":

        # who is the user 
        currentUser = request.user

        listing = Listing.objects.get(pk=id)

        in_watchlist = Watchlist.objects.filter(user=currentUser, item=listing).exists()

        comment = Comments.objects.filter(listing=listing)


        return render(request, "auctions/informations.html",{
            "listing":listing, 
            "comments":comment,
            "watchilist": in_watchlist

        })
    else:
        pass
    
def SaveComment(request,id):
    if request.method == "POST":
        
        # who is the user
        currentUser = request.user

        comment = request.POST['NewComment']

        listing = Listing.objects.get(pk=id)

        new_comment = Comments.objects.create(author=currentUser,listing=listing,comments=comment)     

        new_comment.save() 

        return HttpResponseRedirect(reverse('morInfomations', args=(id,)))



def addWatchlist(request,id):

    if request.method == "POST":


        # who is the user
        currentUser =  request.user
        
        # pegando a lista do usario
        watchlist = Watchlist.objects.filter(user=currentUser)

        # legando o objce
        listing = Listing.objects.get(pk=id)

        # adicionando 
        watchlist.item.add(listing)

        # Redirect or render a success message

        return HttpResponseRedirect(reverse("morInfomations",args=(id, )))

    

def removeWatchlist(request,id):

    if request.method == "POST":

        print(id)
        # who is the user
        currentUser =  request.user
        
        # pegando a lista do usario
        watchlist = Watchlist.objects.filter(user=currentUser)

        # legando o objce
        listing = Listing.objects.get(pk=id)

        # removendo
        watchlist.item.remove(listing)

        return HttpResponseRedirect(reverse("morInfomations",args=(id, )))


def Watchilist(request):
    pass

def newBid(request,id):
    if request.method == "POST":
      
      newbid =  request.POST['new_bid']

      listing = Listing.objects.get(pk=id)

      if int(newbid) > listing.price.bid:
           
        # update table bid 
        UpdateBid = Bid(bid_user=request.user,bid=newBid)

        UpdateBid.save()

        listing.price = UpdateBid

        listing.save()

        return render(request,"auctions/informations.html",{
            "listing":listing,
            "mensage":"Bid was updated.",
            "update":True
        })
    else:
        return render(request,"auctions/informations.html",{
        "listing":listing,
        "mensage":"Bid upadated faled!",
        "update":False
    })
    return HttpResponseRedirect(reverse("morInfomations",args=(id, )))

          





           




