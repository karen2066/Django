from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^market/$', views.market, name='market'),
    url(r'^market/(\d+)/(\d+)/(\d+)', views.user_market, name='market_params'),
    url(r'^addCart/', views.add_cart, name='addCart'),
    url(r'^subCart/', views.sub_cart, name='subCart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^changeSelectStatus/', views.change_select_status, name='change_select_status'),
    url(r'^generateOrder/', views.generate_order, name='generate_Order'),
    url(r'^changeOrderStatus/', views.change_order_status, name='change_order_status'),
    url(r'^waitPay/', views.order_wait_pay, name='order_wait_pay'),
    url(r'^payed/', views.order_payed, name='order_payed'),
    url(r'^waitPaytoPayed/', views.wait_pay_to_payed, name='wait_pay_to_payed'),

]

