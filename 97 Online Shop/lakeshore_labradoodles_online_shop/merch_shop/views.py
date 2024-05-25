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
    cart = request.session.get('cart')
    cart = shop.get_cart(cart)
    return render(request, 'cart.html', {'cart': cart})


def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = request.session.get('cart')
        if cart == None:
            cart = {
                'items': {},
                'order_total': 0,
            }
        variant = shop.get_variant(
            request.POST['product_id'],
            request.POST['color'],
            request.POST['size'],
        )
        cart['items'][variant['id']] = 1
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')
    return 'Could not add to cart.'  # TODO: add better error handling


def remove_from_cart(request: HttpRequest, variant_id):
    cart = request.session.get('cart')
    if cart == None:
        cart = {}
    cart['items'].pop(str(variant_id))
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def update_quantity(request: HttpRequest):
    if request.method == 'POST':
        variant_id = request.POST['variant_id']
        quantity = request.POST['quantity']
        cart = request.session.get('cart')
        if cart == None:
            cart = {}
        cart['items'][variant_id] = quantity
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')
    return 'Could not add to cart.'  # TODO: add better error handling


def checkout(request: HttpRequest):
    # try:
    cart = request.session.get('cart')
    checkout_session = shop.checkout(cart)
    return redirect(checkout_session.url)
    # except Exception as e:
    #     return str(e)


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
