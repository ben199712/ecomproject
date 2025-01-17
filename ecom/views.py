import requests
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def index(request, category_slug=None):
    category_page = None
    products = None
    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)
    
    return render(request, 'index.html', {'category':category_page, 'products':products})


def productPage(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'product.html', {'product':product})


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart =Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    
    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    
    if request.method == "POST":
        # Initiate Paystack Payment
        email = request.user.email  # Assuming you have user authentication
        amount = int(total * 100)  # Paystack expects amount in kobo (100 kobo = 1 Naira)

        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }

        data = {
            "email": email,
            "amount": amount,
            "callback_url": "http://127.0.0.1:8000/payment/callback/",  # Adjust callback URL to your actual URL
        }

        response = requests.post(f'{settings.PAYSTACK_BASE_URL}/transaction/initialize', json=data, headers=headers)
        response_data = response.json()

        if response_data['status']:
            authorization_url = response_data['data']['authorization_url']
            return redirect(authorization_url)
        else:
            return render(request, 'error.html', {'message': 'Payment initialization failed.'})

    return render(request, 'cart.html', dict(cart_items = cart_items, total = total, counter = counter))


# Callback for paystack payment verification

def payment_callback(request):
    reference = request.GET.get('reference')

    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }

    response = requests.get(f'{settings.PAYSTACK_BASE_URL}/transaction/verify/{reference}', headers=headers)
    response_data = response.json()

    if response_data['status'] and response_data['data']['status'] == 'success':
        # Payment was successful
        return JsonResponse({'message': 'Payment successful!'})
    else:
        # Payment failed
        return JsonResponse({'error': 'Payment verification failed.'})


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')

