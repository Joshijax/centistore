from django.urls import path

from dashboard.views import DashboardHomeView
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    HomeView2,
    OrderSummaryView,
    add_to_cart,
    confirm_payment,
    remove_from_cart,
    remove_single_item_from_cart,
    # PaymentView,
    AddCouponView,
    RequestRefundView,
    ShopView,
    logout_request,
    ItemDetailView1,
    OrderSummaryView2,
    CheckoutView1,
    payment_response,
    SearchView,
    CategoryArticlesListView,
    add_first_to_cart,
    SubmitLocation
)

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('home/', HomeView2.as_view(), name='home2'),
    path('home/', HomeView2.as_view(), name='home2'),
    path('logout/', logout_request, name='logout'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('submit_location/', SubmitLocation.as_view(), name='submit_location'),
    path('checkout1/', CheckoutView1.as_view(), name='checkout1'),
    path('callback', payment_response, name='payment_response'),
    path('confirm', confirm_payment, name='confirm'),
    path('shop/', ShopView.as_view(), name='shop'),
    path(
        route='category/<str:slug>/<str:cate>',
        view=CategoryArticlesListView.as_view(),
        name='category_prod'
    ),
    path('search/', SearchView.as_view(), name='search'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('order-summary1/', OrderSummaryView2.as_view(), name='order-summary1'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('product1/<slug>/', ItemDetailView1.as_view(), name='product1'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-first-to-cart/<slug>/', add_first_to_cart, name='add-first-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),
    # path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
