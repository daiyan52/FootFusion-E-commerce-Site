from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView

from App_shop.models import Product,Category

class HomeView(ListView):
    model = Product
    template_name = 'App_shop/home.html'

# class ProductDetailView(LoginRequiredMixin, DetailView):
#     model = Product
#     template_name = 'App_shop/productdetails.html'
class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'App_shop/productdetails.html'

@login_required
def seeDetails(request):
    return render(request, 'App_shop/productdetails.html')

