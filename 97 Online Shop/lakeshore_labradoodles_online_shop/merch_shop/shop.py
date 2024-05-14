from decimal import Decimal
import os
from django.http import HttpRequest
import requests
import stripe
from .models import Product, Variant, Color, Price

PRINTFUL_AUTH_TOKEN = os.getenv('PRINTFUL_AUTH_TOKEN')
STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')


class Printful():
    '''A class that interacts with the Printful API. Initialize with store specific auth token from Printful to link this object with your store.'''

    def __init__(self, auth_token: str) -> None:
        self.auth_token = auth_token
        self.api_endpoint = 'https://api.printful.com/'
        self.api_headers = {
            'Authorization': 'Bearer ' + self.auth_token
        }

    def get_all_products(self) -> list[dict]:
        '''Returns all sync products from the Printful shop.'''
        response = requests.get(
            url=self.api_endpoint + 'sync/products',
            headers=self.api_headers,
            params={'status': 'all'},
        )
        return response.json()['result']

    def get_product(self, id: int | str) -> dict:
        '''Takes a Printful sync product ID as an input and returns details on the product.'''
        response = requests.get(
            url=self.api_endpoint + 'sync/products/' + str(id),
            headers=self.api_headers,
            params={'limit': 100},
        )
        return response.json()['result']

    def get_variant_ids(self, id: int | str) -> dict:
        '''Takes a Printful sync product ID as an input and returns details on all its variants.'''
        product = self.get_product(id)
        variants_ids = [variant['id'] for variant in product['sync_variants']]
        return variants_ids

    def get_variant(self, id: int | str) -> dict:
        '''Takes a Printful sync variant ID as an input and returns details on that variant.'''
        response = requests.get(
            url=self.api_endpoint + 'store/variant/' + id,
            headers=self.api_headers,
        )
        return response.json()['result']['sync_variant']

    def get_color_code(self, id: int | str) -> str:
        '''Takes a Printful product variant ID as an input and returns the color code associated with that variant.'''
        response = requests.get(
            url=self.api_endpoint + 'products/variant/' + id,
            headers=self.api_headers,
        )
        return response.json()['result']['variant']['color_code']


class Stripe():
    '''A class that interacts with the Stripe API. Initialize with Stripe API key to link this object with your account.'''

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = self.api_key

    def get_price(self, id):
        '''Takes a Printful variant ID as an input and returns a stripe price object.'''
        stripe.Price.search(
            query=f"active:'true' AND metadata['printful_variant_id']:'{id}'")


class Shop():
    def __init__(self) -> None:
        self.printful = Printful(PRINTFUL_AUTH_TOKEN)
        self.stripe = Stripe(STRIPE_API_KEY)

    def get_all_products(self) -> list[Product]:
        try:
            syncs = self.printful.get_all_products()
            products = []
            for sync in syncs:
                # Get product from database or create it if it doesn't exist.
                try:
                    product = Product.objects.get(id=sync['id'])
                except Product.DoesNotExist:
                    product = self.create_product(sync['id'])
            products.append(product)
        except:
            products = []
        return products

    def create_product(self, product_id: int | str) -> Product:
        '''Takes Printful product ID as an input and creates a product entry in the database.'''
        sync = self.printful.get_product(product_id)
        variants = []
        colors = []
        sizes = []

        # Create variants
        for sync_variant in sync['sync_variants']:
            # Get variant from database or create it if it doesn't exist.
            try:
                variant = Variant.objects.get(id=sync_variant['id'])
            except Variant.DoesNotExist:
                variant = self.create_variant(sync_variant)

            variants.append(variant)

        # Get colors from database or create it if it doesn't exist.
        color_names = set([variant['color']
                          for variant in sync['sync_variants']])

        new_product = Product.objects.create(
            id=id,
            colors=colors,
            sizes=set([variant['size'] for variant in sync['sync_variants']]),
        )
        return new_product

    def create_variant(self, sync_variant):
        '''Takes Printful sync_variant details as an input and creates a variant entry in the database.'''
        # Get color from database or create
        try:
            color = Color.objects.get(name=sync_variant['color'])
        except Color.DoesNotExist:
            color = Color.objects.create(
                name=sync_variant['color'],
                code=self.printful.get_color_code(
                    sync_variant['product']['variant_id']),
            )
        # Get price from database or create
        try:
            price = Price.objects.get(name=sync_variant['Price'])
        except Price.DoesNotExist:
            price = Price.objects.create(
                id=self.stripe.get_price(),
                value=Decimal(sync_variant['retail_price']),
            )
        # Write to database
        variant = Variant.objects.create(
            id=sync_variant['id'],  # Printful variant ID
            product=sync_variant['sync_product_id'],
            price=Decimal(sync_variant['retail_price']),
            color=color,
            size=sync_variant['size'],
        )
        return variant

    def get_product(self, id) -> Product:
        pass

    def get_cart(self, cart):
        if cart == None:
            cart = {
                'order_total': 0
            }
        else:
            for variant_id in cart:
                cart_item = self.printful.get_variant(variant_id)
                cart[variant_id] = {
                    'name': cart_item['name'],
                    'price': float(cart_item['retail_price']),
                    'total_price': float(cart_item['retail_price']) * int(cart[variant_id]['quantity']),
                    'img': cart_item['files'][0]['thumbnail_url'],
                    'quantity': cart[variant_id]['quantity'],
                }
            cart['order_total'] = sum([cart[id]['total_price'] for id in cart])
        return cart

    def checkout(self) -> stripe.checkout.Session:
        YOUR_DOMAIN = 'http://localhost:8000'
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # TODO: Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': 'price_1PFnsqP92FIWHIYqCtsqnYwE',
                    'quantity': 1,
                }, {
                    'price': 'price_1PFnj9P92FIWHIYqw1lX9yKt',
                    'quantity': 3,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cart',
        )
        return checkout_session
