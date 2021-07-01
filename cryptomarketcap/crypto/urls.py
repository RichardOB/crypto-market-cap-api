from django.urls import path
from django.views.decorators.cache import cache_page

from crypto import views

app_name = 'crypto'

urlpatterns = [
    path(
        'coinList/',
        cache_page(60*60*12)(views.CoinListViewSet.as_view({'get': 'list'})),
        name='coinList'
    ),
]
