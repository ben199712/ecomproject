"""
URL configuration for ecompro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ecom.views import index, productPage, cart_detail, add_cart, cart_remove, remove_product, payment_callback
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('category/<slug:category_slug>', index, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', productPage, name='product_detail'),
    path('cart/add/<int:product_id>,', add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>,', cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>,', remove_product, name='remove_product'),
    path('cart', cart_detail, name='cart_detail'),
     path('payment/callback/', payment_callback, name='payment_callback'),  # Handle payment callback
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)