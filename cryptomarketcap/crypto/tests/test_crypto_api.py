from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from crypto.constants import INVALID_DATE, COIN_UNAVAILABLE, \
    COIN_ID_NOT_PROVIDED, QUERY_DATE_NOT_PROVIDED, \
    CURRENCY_CODE_NOT_PROVIDED, FUTURE_DATE_NOT_ALLOWED


GET_COINLIST_URL = reverse('crypto:coinList')
GET_MARKET_CAP_URL = reverse('crypto:marketCap')


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

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_success(self, coin_gecko):
        """Test that the market cap is returned successfully for a given coin,
        date and currency"""

        coin_id = 'ripple'
        date = '2021/05/03'
        currency = 'gbp'

        expected_currency_value = 62391934063.9954

        coin_gecko.get_coin_history_by_id.return_value = {
            "market_data": {
                "market_cap": {
                    "aed": 309664574594.0909,
                    "ars": 1569030671572.87,
                    "aud": 107997065327.799,
                    "gbp": 62391934063.9954,
                }
            }
        }

        response = self.client.get(
            GET_MARKET_CAP_URL,
            {'coin_id': coin_id, 'date': date, 'currency': currency}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[currency], expected_currency_value)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_missing_coin_id(self, coin_gecko):
        """Test that a coin id is required to fetch market cap data for a given
        currency and date"""

        date = '2021/05/03'
        currency = 'gbp'

        response = self.client.get(
            GET_MARKET_CAP_URL, {'date': date, 'currency': currency})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], COIN_ID_NOT_PROVIDED)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 0)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_missing_date(self, coin_gecko):
        """Test that a date is required to fetch market cap data for a given
        coin and currency"""

        coin_id = 'ripple'
        currency = 'gbp'

        response = self.client.get(
            GET_MARKET_CAP_URL, {'coin_id': coin_id, 'currency': currency})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], QUERY_DATE_NOT_PROVIDED)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 0)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_missing_currency_code(self, coin_gecko):
        """Test that a currency code is required to fetch market cap data for a given
        coin id and date"""

        coin_id = 'ripple'
        date = '2021/05/03'

        response = self.client.get(
            GET_MARKET_CAP_URL, {'coin_id': coin_id, 'date': date})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], CURRENCY_CODE_NOT_PROVIDED)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 0)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_invalid_query_date(self, coin_gecko):
        """Test that a valid query date is required to fetch market cap data for a
        given coin and currency"""

        coin_id = 'ripple'
        date = '2021-05-03'
        currency = 'gbp'

        response = self.client.get(
            GET_MARKET_CAP_URL,
            {'coin_id': coin_id, 'date': date, 'currency': currency}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], INVALID_DATE)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 0)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_future_date(self, coin_gecko):
        """Test that a future query date is not allowed when fetching market
        cap data for a given coin and currency"""

        coin_id = 'ripple'
        date = '2022/05/03'
        currency = 'gbp'

        response = self.client.get(
            GET_MARKET_CAP_URL,
            {'coin_id': coin_id, 'date': date, 'currency': currency}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], FUTURE_DATE_NOT_ALLOWED)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 0)

    @patch('crypto.views.coinGeckoAPI')
    def test_get_market_cap_coin_id_unavailable(self, coin_gecko):
        """Test that a listed coin id is required to fetch market cap data for
        a given currency and date"""

        coin_id = 'unavailable'
        date = '2021/05/03'
        currency = 'gbp'

        coin_gecko.get_coin_history_by_id.side_effect = ValueError

        response = self.client.get(
            GET_MARKET_CAP_URL,
            {'coin_id': coin_id, 'date': date, 'currency': currency}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], COIN_UNAVAILABLE)
        self.assertEqual(coin_gecko.get_coin_history_by_id.call_count, 1)
