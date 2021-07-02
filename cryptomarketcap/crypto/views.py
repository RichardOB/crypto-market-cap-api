from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from pycoingecko import CoinGeckoAPI
from crypto.serializers import CoinGeckoMarketChartResponseSerializer

from crypto.constants import INVALID_DATE, COIN_UNAVAILABLE, \
    COIN_ID_NOT_PROVIDED, QUERY_DATE_NOT_PROVIDED, \
    CURRENCY_CODE_NOT_PROVIDED, FUTURE_DATE_NOT_ALLOWED

import datetime

coinGeckoAPI = CoinGeckoAPI()


class CoinListViewSet(viewsets.ViewSet):
    """Interact with list of coins at Coin Gecko"""

    def list(self, request):
        """List all supported coins id, name and symbol"""
        response = coinGeckoAPI.get_coins_list()
        return Response(response)

    def market(self, request):
        """Returns a JSON response containing the market cap for the given coin_id,
         in the given currency, on the given date"""

        coin_id = self.request.query_params.get('coin_id')
        date_str = self.request.query_params.get('date')
        currency = self.request.query_params.get('currency')

        self.validate_request_params(coin_id, date_str, currency)

        try:
            date = datetime.datetime.strptime(date_str, "%Y/%m/%d").date()
            date_request_str = date.strftime('%d-%m-%Y')
        except ValueError:
            raise ParseError(INVALID_DATE)

        if date > date.today():
            raise ParseError(FUTURE_DATE_NOT_ALLOWED)

        try:
            response = coinGeckoAPI.get_coin_history_by_id(
                id=coin_id, date=date_request_str, localization=False)
        except ValueError:
            raise ParseError(COIN_UNAVAILABLE)

        marketChartResponse = CoinGeckoMarketChartResponseSerializer(
            response).data

        market_Cap = marketChartResponse['market_data']['market_cap'][currency]

        response = {
            currency: market_Cap
        }

        return Response(response)

    def validate_request_params(self, coin_id, date_str, currency):
        if not coin_id:
            raise ParseError(COIN_ID_NOT_PROVIDED)

        if not date_str:
            raise ParseError(QUERY_DATE_NOT_PROVIDED)

        if not currency:
            raise ParseError(CURRENCY_CODE_NOT_PROVIDED)
