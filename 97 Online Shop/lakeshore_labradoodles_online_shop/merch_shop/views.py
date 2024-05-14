import stripe
import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .models import Product, Variant
import requests as req
import os
from dotenv import load_dotenv
from .shop import Shop
load_dotenv()

shop = Shop()


# VIEWS
def home(request: HttpRequest):
    products = shop.get_all_products()
    return render(request, 'index.html', {'products': products})


def product(request: HttpRequest, product_id):
    product = shop.get_product(int(product_id))
    return render(request, 'product.html', {'product': product})


def cart(request: HttpRequest):
    cart_cookies = request.session.get('cart')
    cart = shop.get_cart(cart_cookies)
    return render(request, 'cart.html', {'cart': cart})


def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = request.session.get('cart')
        if cart == None:
            cart = {}
        cart[request.POST['variant_id']] = {
            # TODO: fix this
            'price': '{{PRICE_ID}}',
            'quantity': 1,
        }
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')


def remove_from_cart(request: HttpRequest, variant_id):
    cart = request.session.get('cart')
    if cart == None:
        cart = {}
    cart.pop(str(variant_id))
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def checkout(request: HttpRequest):
    try:
        checkout_session = shop.checkout()
        return redirect(checkout_session.url)
    except Exception as e:
        return str(e)


def success(request: HttpRequest):
    return redirect('success')


# TODO: decide how to reconcile printful/stripe APIs
# link printful product_id to stripe metadata?
# how many extra API calls will this require?
# would it be better to store it in a database? if so, how to maintain?

# TODO: display all products on home page
# TODO: display product info on product page
# TODO: get stripe price ids based on size (use price_data to dynamically create price (default + size bonus))
# TODO: add ids to cart/cookies (how to keep track of color for ordering from printful? db model that connects printful/stripe ids)

# TODO: CHECKOUT SESSION SHOULD CREATE PRODUCTS INLINE SO THAT PRODUCT DATA DOESN'T HAVE TO BE UPDATED ON BOTH PRINTFUL AND STRIPE.
