from django.urls import path
from orders import views

urlpatterns=[
    path('post_fast_order/',views.PostFastOrder),
    path('post_order/',views.PostOrder),
    path('profile/', views.ProfileOrders),

    # path('order/edit/',views.OrderStatusEdit.as_view(),name='order_status_edit'),
    # path('fast_orders/',views.AllFastOrderView.as_view(),name='AllFastOrderView'),
    # path('Username_checkView/',views.Username_checkView.as_view(),name='Username_checkView'),

    # path('kaspi/<int:order_id>/',views.OrderPay.as_view(),name='kaspi'),
]