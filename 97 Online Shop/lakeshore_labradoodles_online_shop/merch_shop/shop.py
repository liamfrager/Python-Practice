from decimal import Decimal
import os
import requests
import stripe
from .models import Product, Variant, Color

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

    def get_product(self, id: int) -> dict:
        '''Takes a Printful sync product ID as an input and returns details on the product.'''
        response = requests.get(
            url=self.api_endpoint + 'sync/products/' + str(id),
            headers=self.api_headers,
            params={'limit': 100},
        )
        return response.json()['result']

    def get_variant_ids(self, id: int) -> dict:
        '''Takes a Printful sync product ID as an input and returns details on all its variants.'''
        product = self.get_product(id)
        variants_ids = [variant['id'] for variant in product['sync_variants']]
        return variants_ids

    def get_variant(self, id: int) -> dict:
        '''Takes a Printful sync variant ID as an input and returns details on that variant.'''
        response = requests.get(
            url=self.api_endpoint + 'store/variant/' + str(id),
            headers=self.api_headers,
        )
        return response.json()['result']['sync_variant']

    def get_color_code(self, id: int) -> str:
        '''Takes a Printful product variant ID as an input and returns the color code associated with that variant.'''
        response = requests.get(
            url=self.api_endpoint + 'products/variant/' + str(id),
            headers=self.api_headers,
        )
        return response.json()['result']['variant']['color_code']


class Stripe():
    '''A class that interacts with the Stripe API. Initialize with Stripe API key to link this object with your account.'''

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        stripe.api_key = self.api_key

    def get_price(self, id) -> stripe.SearchResultObject[stripe.Price]:
        '''Takes a Printful variant ID as an input and returns a stripe price object.'''
        price = stripe.Price.search(
            query=f"active:'true' AND metadata['printful_product_id']:'{id}'")
        if price['data'] == []:
            price = self.create_price()
        print(price)
        return price

    def create_price(self):
        stripe.Price.create(
            currency="usd",
            unit_amount=1000,
            product_data={"name": "Gold Plan"},
        )


class Shop():
    def __init__(self) -> None:
        self.printful = Printful(PRINTFUL_AUTH_TOKEN)
        self.stripe = Stripe(STRIPE_API_KEY)

    def get_all_products(self) -> list[Product]:
        '''Returns all product entries in the database or creates them if they don't exist.'''
        # try:
        syncs = self.printful.get_all_products()
        products = []
        for sync in syncs:
            product = Product(
                id=sync['id'],
                name=sync['name'],
                image=sync['thumbnail_url'],
            )
            products.append(product)
        return products

    def get_product(self, id: int) -> Product:
        '''Takes Printful sync product ID as an input and returns its entry in the database or creates it if it doesn't exist.'''
        sync = self.printful.get_product(id)

        # Create product object
        product = Product(
            id=id,
            name=sync['sync_product']['name'],
            image=sync['sync_product']['thumbnail_url'],
            sizes=set([variant['size'] for variant in sync['sync_variants']]),
        )

        # Get product colors
        colors = []
        for variant in sync['sync_variants']:
            # Get color from database or create
            try:
                color = Color.objects.get(name=variant['color'])
            except Color.DoesNotExist:
                color = Color.objects.create(
                    name=variant['color'],
                    code=self.printful.get_color_code(
                        variant['product']['variant_id']),
                )
            colors.append(color)
        product.colors.set(set(colors))  # add unique colors to product object
        return product

        # # Create variants for product (must be done after the entry for the product is created).
        # variants: list[Variant] = []
        # for sync_variant in sync['sync_variants']:
        #     # Get variant from database or create it if it doesn't exist.
        #     variant = Variant(
        #         id=sync_variant['id'],  # Printful variant ID
        #         product=product,
        #         price=Decimal(sync_variant['retail_price']),
        #         color=color,
        #         size=sync_variant['size'],
        #     )
        #     variants.append(variant)
        # return product, variants

    def get_cart(self, cart) -> dict:
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
        # TODO: verify that all items in the cart still exist/are in stock through printful.
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


# TODO: rewrite all functions to not draw from database but straight from Printful. Should create model objects without saving to the database.
