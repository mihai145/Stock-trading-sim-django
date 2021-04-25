import requests
import json

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from .models import User, Stocks, Transaction

from django import forms


class SearchForm(forms.Form):
    ticker = forms.CharField(label='Ticker', max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Stock Ticker'}))


def valid(ticker):
    # Ckeck weather the ticker from the json-response does not contain invalid characters
    for chr in ticker:
        if chr < 'A' or chr > 'Z':
            return False

    return True


def index(request):
    # Request (30) stocks for FinnHub
    r = requests.get(
        'https://finnhub.io/api/v1/stock/symbol?exchange=US&token=YOUR_API_KEY')

    data = r.json()
    stocks = []
    for stock in data:
        if len(stocks) >= 30:
            break
        else:
            if valid(stock["symbol"]):
                stocks.append(
                    {"symbol": stock["symbol"], "name": stock["description"]})

    return render(request, "stocks/index.html", {
        "stocks": stocks,
        "searchform": SearchForm
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
            return render(request, "stocks/login.html", {
                "message": "Invalid username and/or password.",
                "searchform": SearchForm
            })
    else:
        return render(request, "stocks/login.html", {
            "searchform": SearchForm
        })


def logout_view(request):
    # Log user out
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "stocks/register.html", {
                "message": "Passwords must match.",
                "searchform": SearchForm
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "stocks/register.html", {
                "message": "Username already taken.",
                "searchform": SearchForm
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "stocks/register.html", {
            "searchform": SearchForm
        })


def stock_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect(reverse('stock_view', args=[form.cleaned_data['ticker']]))

    return HttpResponseRedirect(reverse("index"))


def stock_view(request, symbol):
    symbol = symbol.upper()

    stocks_owned = 0
    if request.user:
        try:
            stocks = Stocks.objects.get(owner=request.user, ticker=symbol)
            stocks_owned = stocks.quantity
        except:
            pass

    r = requests.get(
        f'https://finnhub.io/api/v1/quote?symbol={symbol}&token=YOUR_API_KEY')

    data = r.json()

    return render(request, "stocks/stock.html", {
        "symbol": symbol,
        "c": data["c"],
        "o": data["o"],
        "l": data["l"],
        "h": data["h"],
        "pc": data["pc"],
        "searchform": SearchForm,
        "owned": stocks_owned
    })


@login_required
def profile_view(request):
    return render(request, "stocks/profile.html", {
        "searchform": SearchForm
    })


@csrf_exempt
@login_required
def invest(request):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("amount"))

        if amount > 0:
            request.user.capital += amount
            request.user.save()
            return JsonResponse({"message": "OK"}, status=201)
        else:
            return JsonResponse({"message": "Invalid request(expected positive amount)"}, status=201)

    return JsonResponse({"message": "Invalid request(expected POST)."}, status=201)


@csrf_exempt
@login_required
def buy(request, symbol):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("amount"))
        pricePerShare = int(data.get("pricePerShare"))

        if amount < 0:
            return JsonResponse({"message": "Invalid request(expected positive amount)"}, status=201)

        toPay = amount * pricePerShare

        if toPay > request.user.capital:
            return JsonResponse({"message": "Insufficient funds"}, status=201)

        request.user.capital -= toPay
        request.user.total_invested += toPay
        request.user.save()

        Transaction.objects.create(
            owner=request.user, ticker=symbol, quantity=amount, sum=toPay)

        try:
            stocks = Stocks.objects.get(owner=request.user, ticker=symbol)
            stocks.quantity += amount
            stocks.save()
        except:
            Stocks.objects.create(owner=request.user,
                                  ticker=symbol, quantity=amount)

        return JsonResponse({"message": "OK"}, status=201)

    return JsonResponse({"message": "Invalid request(expected POST)."}, status=201)


@csrf_exempt
@login_required
def sell(request, symbol):
    if request.method == "POST":
        data = json.loads(request.body)
        amount = int(data.get("amount"))
        pricePerShare = int(data.get("pricePerShare"))

        if amount < 0:
            return JsonResponse({"message": "Invalid request(expected positive amount)"}, status=201)

        try:
            stocks = Stocks.objects.get(owner=request.user, ticker=symbol)

            if stocks.quantity < amount:
                return JsonResponse({"message": "Insufficient shares owned"}, status=201)

            stocks.quantity -= amount
            stocks.save()

            toReceive = amount * pricePerShare

            request.user.capital += toReceive
            request.user.total_sold += toReceive
            request.user.save()

            Transaction.objects.create(
                owner=request.user, ticker=symbol, quantity=-amount, sum=toReceive)

            return JsonResponse({"message": "OK"}, status=201)

        except:
            return JsonResponse({"message": "Insufficient shares owned"}, status=201)

    return JsonResponse({"message": "Invalid request(expected POST)."}, status=201)
