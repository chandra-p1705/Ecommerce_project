from django.shortcuts import render,redirect
from .models import Product


def home(request):
    products= Product.objects.all()
    return render(request, 'home.html', {
        'products':products
        
    })
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1
    request.session['cart'] = cart

    return redirect('home')
def cart(request):
    cart_data = request.session.get('cart', {})

    cart_items = []

    for product_id, quantity in cart_data.items():
        product = Product.objects.get(id=product_id)

        cart_items.append({
            'product': product,
            'quantity': quantity
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items
    })

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

