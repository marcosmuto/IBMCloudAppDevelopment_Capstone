from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, analyze_review_sentiments, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    context = {}
    return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

def registration(request):
    context = {}
    return render(request, 'djangoapp/registration.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index', context)
    else:
        return render(request, 'djangoapp/index', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp:index', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://43bb4759.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        #dealer_names = '<br>'.join([dealer.short_name for dealer in dealerships])
        context["dealerships"] = dealerships
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

def get_dealership(dealer_id):
    dealership = None
    
    url = "https://43bb4759.us-south.apigw.appdomain.cloud/api/dealership"
    dealerships = get_dealers_from_cf(url)

    for dealer in dealerships:
        if dealer.id == dealer_id:
            dealership = dealer
    
    return dealership

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://43bb4759.us-south.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        
        # Get dealer data
        dealer = get_dealership(dealer_id)

        # Add data to context
        context["reviews"] = reviews
        context["dealer"] = dealer
        
        # Return a list of dealer short name
        #return HttpResponse(reviewers)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    user = request.user
    if user:
        if request.method == "GET":
            # Get dealer data
            dealer = get_dealership(dealer_id)

            #Get car data
            cars = CarModel.objects.filter(dealer_id = dealer_id)

            # Add data to context
            context["cars"] = cars
            context["dealer"] = dealer

            return render(request, 'djangoapp/add_review.html', context)
        if request.method == "POST":
            car_id = request.POST['car']
            car = CarModel.objects.get(id = car_id)

            review = dict()
            review["id"] = int(datetime.now().timestamp())
            review["name"] = user.username
            review["dealership"] = dealer_id
            review["review"] = request.POST['review']
            review["purchase"] = True if 'purchasecheck' in request.POST else False
            review["purchase_date"] = request.POST['purchasedate'] if 'purchasedate' in request.POST else datetime.now().strftime("%m/%d/%Y")
            review["car_make"] = car.make_id.name
            review["car_model"] = car.name
            review["car_year"] = car.year.strftime("%Y")

            print(review)

            json_payload = dict()
            json_payload["review"] = review

            url="https://43bb4759.us-south.apigw.appdomain.cloud/api/review"

            response = post_request(url, json_payload)

            print(response)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    else:
        return redirect('djangoapp:index')

