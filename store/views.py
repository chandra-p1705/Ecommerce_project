from django.shortcuts import render,redirect
from .models import Product,Order
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def home(request):
    products= Product.objects.all()
    print("PRODUCT COUNT:", products.count(), "DB:", products.db)
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
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        return redirect('cart')

def checkout(request):


    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('cart')

    cart_items = []
    total_price = 0

    for product_id, quantity in cart_data.items():

        product = Product.objects.get(id=product_id)

        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    if request.method == 'POST':

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        order = Order.objects.create(
             user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            pincode=pincode,
            total_price=total_price
        )

        request.session['cart'] = {}

        return render(request, 'order_success.html', {
            'order': order
        })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')
def logout_view(request):
    logout(request)
    return redirect('home')