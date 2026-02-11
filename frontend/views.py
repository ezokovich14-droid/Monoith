from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def products(request):
    return render(request, 'products.html')


def orders(request):
    return render(request, 'orders.html')


def dashboard(request):
    return render(request, 'dashboard.html')
