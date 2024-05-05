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
    # Get colors
    colors = set([variant.color_code for variant in variants])
    colors = [{
        'code': color,
        'name': ProductVariant.objects.filter(color_code=color)[0].color_name,
        'files': next(variant for variant in product['sync_variants'] if variant['color'] == ProductVariant.objects.filter(color_code=color)[0].color_name)['files'],
        'sizes': json.dumps({variant['size']: variant['id'] for variant in product['sync_variants'] if variant['color'] == ProductVariant.objects.filter(color_code=color)[0].color_name})
    } for color in colors]
    # Get sizes
    sizes = set([variant.size for variant in variants])
    sizes = [size for size in ['S', 'M', 'L',
                               'XL', '2XL', '3XL', '4XL'] if size in sizes]
    return render(request, 'product.html', {'product': product['sync_product'], 'variants': product['sync_variants'], 'colors': colors, 'sizes': sizes})


def cart(request: HttpRequest):
    cart = request.session.get('cart')
    if cart != None:
        for variant_id in cart:
            res = req.get(
                url=PRINTFUL_API_ENDPOINT + 'sync/variant/' + variant_id,
                headers=PRINTFUL_API_HEADERS,
            )
            product = res.json()['result']['sync_variant']
            cart[variant_id] = {
                'name': product['name'],
                'price': float(product['retail_price']),
                'total_price': float(product['retail_price']) * int(cart[variant_id]['quantity']),
                'img': product['files'][0]['thumbnail_url'],
                'quantity': cart[variant_id]['quantity'],
            }
        order_total = sum([cart[id]['total_price'] for id in cart])
    else:
        order_total = 0
    return render(request, 'cart.html', {'cart': cart, 'order_total': order_total})


def add_to_cart(request: HttpRequest):
    if request.method == 'POST':
        cart = request.session.get('cart')
        if cart == None:
            cart = {}
        cart[request.POST['variant_id']] = {
            'quantity': 1}
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
