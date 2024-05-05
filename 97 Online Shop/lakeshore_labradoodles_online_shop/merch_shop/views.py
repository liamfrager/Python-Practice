import json
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from .models import ProductVariant
import requests as req
import os
from dotenv import load_dotenv
load_dotenv()

PRINTFUL_AUTH_TOKEN = os.getenv('PRINTFUL_AUTH_TOKEN')
PRINTFUL_API_ENDPOINT = 'https://api.printful.com/'
PRINTFUL_API_HEADERS = {
    'Authorization': 'Bearer ' + PRINTFUL_AUTH_TOKEN
}


# Create your views here.
def home(request: HttpRequest):
    res = req.get(
        url=PRINTFUL_API_ENDPOINT + 'sync/products',
        headers=PRINTFUL_API_HEADERS,
        params={'status': 'synced'}
    )
    products = res.json()['result']
    print(products)
    return render(request, 'index.html', {'products': products})


def product(request: HttpRequest, product_id):
    res = req.get(
        url=PRINTFUL_API_ENDPOINT + 'sync/products/' + str(product_id),
        headers=PRINTFUL_API_HEADERS,
        params={'limit': 100}
    )
    product = res.json()['result']
    variants = []
    for variant in product['sync_variants']:
        variant_id = variant['variant_id']
        try:
            var = ProductVariant.objects.get(variant_id=variant_id)
        except ProductVariant.DoesNotExist:
            res = req.get(
                url=PRINTFUL_API_ENDPOINT +
                'products/variant/' + str(variant_id),
                headers=PRINTFUL_API_HEADERS,
            )
            data = res.json()['result']['variant']
            var = ProductVariant.objects.create(
                variant_id=variant_id,
                color_name=data['color'],
                color_code=data['color_code'],
                size=data['size'],
            )
        finally:
            variants.append(var)

    colors = set([variant.color_code for variant in variants])
    sizes = set([variant.size for variant in variants])
    sizes = [size for size in ['S', 'M', 'L',
                               'XL', '2XL', '3XL', '4XL'] if size in sizes]
    return render(request, 'product.html', {'product': product['sync_product'], 'variants': product['sync_variants'], 'colors': colors, 'sizes': sizes})


def cart(request: HttpRequest):
    cart = request.session.get('cart')
    for product_id in cart:
        product = ProductVariant.objects.get(pk=product_id)
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'total_price': product.price * int(cart[product_id]['amount']),
            'img': product.img,
            'amount': cart[product_id]['amount'],
        }
    order_total = sum([cart[id]['total_price'] for id in cart])
    return render(request, 'cart.html', {'cart': cart, 'order_total': order_total})


def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = request.session.get('cart')
        if cart == None:
            cart = {}
        cart[request.POST['product_id']] = {
            'quantity': request.POST['quantity']}
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')
