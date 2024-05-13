import os
import requests
from .models import Product, Variant


class Printful():
    '''Initialize with store specific auth token from Printful to link this object to your store.'''

    def __init__(self, auth_token: str) -> None:
        self.auth_token = auth_token
        self.api_endpoint = 'https://api.printful.com/'
        self.api_headers = {
            'Authorization': 'Bearer ' + self.auth_token
        }

    def get_all_products(self) -> list[dict]:
        '''Returns all products from the Printful Shop'''
        response = requests.get(
            url=self.api_endpoint + 'sync/products',
            headers=self.api_headers,
            params={'status': 'all'},
        )
        return response.json()['result']

    def get_product(self, id: int | str) -> dict:
        '''Takes a Printful product ID as an input and returns details on the product.'''
        response = requests.get(
            url=self.api_endpoint + 'sync/products/' + str(id),
            headers=self.api_headers,
            params={'limit': 100}
        )
        return response.json()['result']

    def get_variants(self, id: int | str) -> dict:
        '''Takes a Printful product ID as an input and returns details on all its variants.'''
        product = self.get_product(id)

        variants = []
        for variant in product['sync_variants']:
            variant_id = variant['variant_id']
            try:
                var = ProductVariant.objects.get(variant_id=variant_id)
            except ProductVariant.DoesNotExist:
                response = requests.get(
                    url=self.api_endpoint +
                    'products/variant/' + str(variant_id),
                    headers=self.api_headers,
                )
                data = response.json()['result']['variant']
                var = ProductVariant.objects.create(
                    variant_id=variant_id,
                    color_name=data['color'],
                    color_code=data['color_code'],
                    size=data['size'],
                )
            finally:
                variants.append(var)

        return variants

    def get_variant(self, id: int | str) -> dict:
        response = requests.get(
            url=self.api_endpoint + 'store/variant/' + id,
            headers=self.api_headers,
        )

        return response.json()['result']
