from django.urls import path
from .views import AssetListDetail, AssetRetrieveUpdateDestroy, api_root, AssetListSummary

urlpatterns = [
    path('', api_root, name='api-root'),
    path('asset_detail/', AssetListDetail.as_view(), name='asset-detail'),
    path('asset_summary/', AssetListSummary.as_view(), name='asset-summary'),
    path('asset/<int:pk>/', AssetRetrieveUpdateDestroy.as_view(), name='asset-upsert'),
    # path('assets/above-price/<int:min_price>/', AssetAbovePriceAPIView.as_view(), name='assets-above-price'),
]
