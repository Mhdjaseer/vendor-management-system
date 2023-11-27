from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('register/',views.UserCreateAPIView.as_view(),name='register'),

    path('vendors/',views.VendorListCreateView.as_view(),name='vendor-list-create'),
    path('vendors/<int:pk>/',views.VendorListUpdateView.as_view(),name='vendor-get-update'),

    path('purchase_orders/',views.PurchaseOrderListCreateView.as_view(),name='purchase-order-list-create'),
    path('purchase_orders/<int:pk>/',views.PurchaseOrderListUpdateView.as_view(),name='purchase-order-list-update-delete'),

    path('vendors/<int:id>/performance/', views.VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:id>/acknowledge/', views.AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),

    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]
