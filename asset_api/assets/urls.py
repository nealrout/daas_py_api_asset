from django.urls import path
from .views import AssetListCreate, AssetRetrieveUpdateDestroy, api_root

urlpatterns = [
    path('', api_root, name='api-root'),
    path('assets/', AssetListCreate.as_view(), name='asset-list'),
    path('assets/<int:pk>/', AssetRetrieveUpdateDestroy.as_view(), name='asset-detail'),
    # path('assets/above-price/<int:min_price>/', AssetAbovePriceAPIView.as_view(), name='assets-above-price'),
]
