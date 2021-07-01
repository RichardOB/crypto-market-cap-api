from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


GET_COINLIST_URL = reverse('crypto:coinList')


class PublicCryptoApiTests(TestCase):
    """Test the publicly available Crypto API"""

    def setUp(self):
        self.client = APIClient()

    @patch('crypto.views.coinGeckoAPI')
    def test_get_coinlist_success(self, coin_gecko):
        """Test that the coinlist is returned successfully"""

        coin_gecko.get_coins_list.return_value = [
            {'id': 'ripple', 'symbol': 'xrp', 'name': 'XRP'},
            {'id': 'xenon-2', 'symbol': 'xen', 'name': 'Xenon'},
            {'id': 'usechain', 'symbol': 'use', 'name': 'Usechain'}
        ]
        response = self.client.get(GET_COINLIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['id'], 'ripple')
        self.assertEqual(response.data[0]['symbol'], 'xrp')
        self.assertEqual(response.data[0]['name'], 'XRP')
