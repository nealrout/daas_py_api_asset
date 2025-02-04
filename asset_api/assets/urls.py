from django.urls import path
from .views import api_root, AssetListDetail, AssetUpsert, AssetListSummary, AssetListDetailMultiple

urlpatterns = [
    path('', api_root, name='api-root'),
    path('asset_detail/', AssetListDetail.as_view(), name='asset-detail'),
    path('asset/retrieve/', AssetListDetailMultiple.as_view(), name='asset-detail-multiple'),
    path('asset_summary/', AssetListSummary.as_view(), name='asset-summary'),
    path('asset/<int:pk>/', AssetUpsert.as_view(), name='asset-upsert'),
    # path('assets/above-price/<int:min_price>/', AssetAbovePriceAPIView.as_view(), name='assets-above-price'),
]
