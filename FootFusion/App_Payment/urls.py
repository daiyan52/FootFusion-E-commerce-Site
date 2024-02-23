from django.urls import path
from App_Payment import views
app_name = 'App_Payment'

urlpatterns = [
    path('payment/',views.checkoutView, name='payment'),
    path('pay/',views.paymentView, name='pay'),
    path('success/', views.paymentSuccess, name='success'),
    path('order/', views.orderView, name='order'),

]
