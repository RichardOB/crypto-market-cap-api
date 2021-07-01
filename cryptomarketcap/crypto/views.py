from rest_framework import viewsets
from rest_framework.response import Response

from pycoingecko import CoinGeckoAPI
coinGeckoAPI = CoinGeckoAPI()


class CoinListViewSet(viewsets.ViewSet):
    """Interact with list of coins at Coin Gecko"""

    def list(self, request):
        """List all supported coins id, name and symbol"""
        response = coinGeckoAPI.get_coins_list()
        return Response(response)
