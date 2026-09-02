from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# pyrefly: ignore [missing-import]
from .models import Product, Cart, CartItem
from decimal import Decimal

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

def seed_default_products():
    default_products = [
        {
            "name": "Classic Linen Shirt",
            "description": "Premium breathable light linen shirt. Perfect for sunny days and semi-formal wear.",
            "price": 59.00,
            "category": "Men",
            "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=600&auto=format&fit=crop",
            "stock": 25
        },
        {
            "name": "Silk Midi Dress",
            "description": "Elegant flowing olive green silk dress featuring a midi cut and delicate straps.",
            "price": 120.00,
            "category": "Women",
            "image_url": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?q=80&w=600&auto=format&fit=crop",
            "stock": 15
        },
        {
            "name": "Leather Chelsea Boots",
            "description": "Handcrafted brown leather boots with elasticated side panels and durable crepe soles.",
            "price": 145.00,
            "category": "Men",
            "image_url": "https://images.unsplash.com/photo-1638247025967-b4e38f787b76?q=80&w=600&auto=format&fit=crop",
            "stock": 10
        },
        {
            "name": "Minimalist Gold Necklace",
            "description": "Delicate 18k gold-plated chain featuring a tiny geometric pendant.",
            "price": 45.00,
            "category": "Accessories",
            "image_url": "https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?q=80&w=600&auto=format&fit=crop",
            "stock": 40
        },
        {
            "name": "Oversized Cashmere Sweater",
            "description": "Indulgently soft, warm knit cashmere sweater in a relaxed, slouchy silhouette.",
            "price": 98.00,
            "category": "Women",
            "image_url": "https://images.unsplash.com/photo-1574164904299-3a102b110380?q=80&w=600&auto=format&fit=crop",
            "stock": 20
        },
        {
            "name": "Classic Sunglasses",
            "description": "UV protected acetate frame sunglasses in a timeless tortoiseshell pattern.",
            "price": 35.00,
            "category": "Accessories",
            "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?q=80&w=600&auto=format&fit=crop",
            "stock": 30
        }
    ]
    for prod in default_products:
        Product.objects.get_or_create(
            name=prod["name"],
            defaults={
                "description": prod["description"],
                "price": prod["price"],
                "category": prod["category"],
                "image_url": prod["image_url"],
                "stock": prod["stock"]
            }
        )

# View All Products
def product_list(request):
    if Product.objects.count() == 0:
        seed_default_products()
        
    category_filter = request.GET.get('category')
    if category_filter:
        products = Product.objects.filter(category=category_filter)
    else:
        products = Product.objects.all()
        
    return render(request, 'products/product_list.html', {
        'products': products,
        'category_filter': category_filter
    })

# Add Product
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        image_url = request.POST.get('image_url', '')
        stock = request.POST.get('stock', 10)
        category = request.POST.get('category', '')
        
        if not name or not price:
            messages.error(request, "Name and price are required.")
            return render(request, 'products/add_product.html')
            
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            image_url=image_url or "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?q=80&w=600&auto=format&fit=crop",
            stock=stock,
            category=category
        )
        messages.success(request, f"Product '{name}' added successfully!")
        return redirect('products:product_list')
        
    return render(request, 'products/add_product.html')

# Update Product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description', '')
        product.price = request.POST.get('price')
        product.image_url = request.POST.get('image_url', '')
        product.stock = request.POST.get('stock', 10)
        product.category = request.POST.get('category', '')
        
        if not product.name or not product.price:
            messages.error(request, "Name and price are required.")
            return render(request, 'products/edit_product.html', {'product': product})
            
        product.save()
        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect('products:product_list')
        
    return render(request, 'products/edit_product.html', {'product': product})

# Delete Product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    name = product.name
    product.delete()
    messages.success(request, f"Product '{name}' deleted successfully!")
    return redirect('products:product_list')

# Add to Cart
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    messages.success(request, f"Added '{product.name}' to cart.")
    
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('products:product_list')

# View Cart
def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.all().select_related('product')
    
    subtotal = sum(item.total_price for item in items)
    shipping = Decimal('10.00') if subtotal > 0 and subtotal < Decimal('150.00') else Decimal('0.00')
    total = subtotal + shipping
    amount_to_free_shipping = Decimal('150.00') - subtotal if subtotal < Decimal('150.00') else Decimal('0.00')
    
    return render(request, 'products/cart.html', {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'amount_to_free_shipping': amount_to_free_shipping
    })

# Update Cart Item Quantity
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        elif action == 'remove':
            cart_item.delete()
            
    return redirect('products:cart_detail')

# Remove from Cart (direct endpoint)
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('products:cart_detail')

# Checkout View
def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.all()
    
    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('products:product_list')
        
    if request.method == 'POST':
        for item in items:
            if item.product.stock >= item.quantity:
                item.product.stock -= item.quantity
                item.product.save()
        
        items.delete()
        messages.success(request, "Order placed successfully! Thank you for shopping at Fashion.com.")
        return render(request, 'products/checkout.html', {'success': True})
        
    subtotal = sum(item.total_price for item in items)
    shipping = Decimal('10.00') if subtotal > 0 and subtotal < Decimal('150.00') else Decimal('0.00')
    total = subtotal + shipping
    
    return render(request, 'products/checkout.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'success': False
    })

def chatbot_view(request):
    # pyrefly: ignore [missing-import]
    from .chatbot import get_chatbot_response
    
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []
        
    if request.GET.get('clear') == 'true':
        request.session['chat_history'] = []
        request.session.modified = True
        return redirect('products:chatbot')
        
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        if user_message:
            bot_response = get_chatbot_response(user_message)
            
            chat_history = request.session['chat_history']
            chat_history.append({
                'question': user_message,
                'response': bot_response
            })
            request.session['chat_history'] = chat_history
            request.session.modified = True
        return redirect('products:chatbot')
        
    return render(request, 'landing page/index9.html', {
        'chat_history': request.session['chat_history']
    })

