import json
from django.http import HttpRequest
from django.shortcuts import render, redirect
from .models import ShopProduct


# Create your views here.
def home(request: HttpRequest):
    products = ShopProduct.objects.all()
    return render(request, 'index.html', {'products': products})


def product(request: HttpRequest, product_id):
    product = ShopProduct.objects.get(pk=product_id)
    return render(request, 'product.html', {'product': product})


def cart(request: HttpRequest):
    cart = request.session.get('cart')
    for product_id in cart:
        product = ShopProduct.objects.get(pk=product_id)
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
        cart[request.POST['product_id']] = {'amount': request.POST['amount']}
        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')
