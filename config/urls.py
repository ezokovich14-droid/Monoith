"""
URL configuration for ecommerce monolith project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse



def home(request):
    return JsonResponse({
        "message": "API Monolith en ligne",
        "endpoints": [
            "/admin/",
            "/api/users/",
            "/api/products/",
            "/api/orders/"
        ]
    })


urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
]