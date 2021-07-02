from rest_framework import serializers


class CoinGeckoMarketDataSerializer(serializers.Serializer):
    """A serializer for the Coin Gecko Market Data response."""
    market_cap = serializers.DictField()


class CoinGeckoMarketChartResponseSerializer(serializers.Serializer):
    """A serializer for the Coin Gecko Market Chart response."""
    market_data = CoinGeckoMarketDataSerializer()
