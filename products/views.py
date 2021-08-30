from django.shortcuts import render
from datetime import datetime
from products.models import Product, ProductCategory


def index(request):
    context = {'title': 'Geekshop', 'datetime': datetime.now()}
    return render(request, 'products/index.html', context)


def products(request):
    context = {'title': 'Geekshop-catalog', 'datetime': datetime.now(),
               'products': Product.objects.all(),
               'categories': ProductCategory.objects.all(),
               }
    return render(request, 'products/products.html', context)
