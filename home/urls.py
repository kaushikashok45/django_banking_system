from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('customers/',views.CustomerListView.as_view(),name='customers'),
    path('customer/<uuid:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('actionUrl/<uuid:cid>',views.transac,name='actionUrl'),
    path('payment/<uuid:tcid>/<uuid:fcid>',views.pay,name='payment'),
    path('process/<uuid:tcid>/<uuid:fcid>',views.process,name='process'),
]
