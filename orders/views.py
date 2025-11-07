from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from catalog.models import Product

# Create your views here.

@login_required
def cart_view(request):
    """Vista para mostrar el carrito de compras"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'orders/cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    """Vista para agregar productos al carrito"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Obtener la cantidad del formulario (por defecto 1)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            quantity = 1
    except (ValueError, TypeError):
        quantity = 1
    
    if product.stock <= 0:
        messages.error(request, f"El producto {product.name} está agotado.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        # Verificar que no exceda el stock disponible
        new_quantity = cart_item.quantity + quantity
        if new_quantity <= product.stock:
            cart_item.quantity = new_quantity
            cart_item.save()
            messages.success(request, f"Se agregaron {quantity} unidades de {product.name} al carrito.")
        else:
            available = product.stock - cart_item.quantity
            if available > 0:
                cart_item.quantity = product.stock
                cart_item.save()
                messages.warning(request, f"Solo se pudieron agregar {available} unidades de {product.name}. Stock máximo alcanzado.")
            else:
                messages.warning(request, f"Ya tienes el stock completo de {product.name} en tu carrito.")
    else:
        # Verificar que la cantidad inicial no exceda el stock
        if quantity > product.stock:
            cart_item.quantity = product.stock
            cart_item.save()
            messages.warning(request, f"Solo hay {product.stock} unidades disponibles de {product.name}.")
        else:
            messages.success(request, f"Se agregaron {quantity} unidades de {product.name} al carrito.")
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@require_POST
def update_cart_item(request, item_id):
    """Vista para actualizar la cantidad de un item del carrito"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    try:
        new_quantity = int(request.POST.get('quantity', 1))
        
        if new_quantity <= 0:
            return remove_from_cart(request, item_id)
        
        if new_quantity > cart_item.product.stock:
            messages.warning(request, f"Solo hay {cart_item.product.stock} unidades disponibles de {cart_item.product.name}.")
            new_quantity = cart_item.product.stock
        
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f"Cantidad actualizada para {cart_item.product.name}.")
        
    except ValueError:
        messages.error(request, "Cantidad inválida.")
    
    return redirect('orders:cart')


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Vista para remover un item del carrito"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f"Se eliminó {product_name} del carrito.")
    
    return redirect('orders:cart')


@login_required
def cart_count(request):
    """Vista AJAX para obtener el conteo de items del carrito"""
    try:
        cart = Cart.objects.get(user=request.user)
        count = cart.get_total_items()
    except Cart.DoesNotExist:
        count = 0
    
    return JsonResponse({'count': count})


@login_required
def checkout_view(request):
    """Vista para el proceso de checkout"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('orders:cart')
    except Cart.DoesNotExist:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('orders:cart')
    
    # Obtener direcciones de envío del usuario
    shipping_addresses = request.user.shipping_addresses.all()
    
    if request.method == 'POST':
        shipping_address_id = request.POST.get('shipping_address')
        
        if not shipping_address_id:
            messages.error(request, "Debe seleccionar una dirección de envío.")
        else:
            # Guardar la dirección seleccionada en la sesión
            request.session['selected_shipping_address'] = shipping_address_id
            return redirect('orders:payment')
    
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_addresses': shipping_addresses,
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def payment_view(request):
    """Vista para procesar el pago"""
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            messages.warning(request, "Tu carrito está vacío.")
            return redirect('orders:cart')
    except Cart.DoesNotExist:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('orders:cart')
    
    # Verificar que se haya seleccionado una dirección de envío
    shipping_address_id = request.session.get('selected_shipping_address')
    if not shipping_address_id:
        messages.error(request, "Debe seleccionar una dirección de envío.")
        return redirect('orders:checkout')
    
    try:
        from accounts.models import ShippingAddress
        shipping_address = ShippingAddress.objects.get(
            id=shipping_address_id, 
            user=request.user
        )
    except ShippingAddress.DoesNotExist:
        messages.error(request, "Dirección de envío inválida.")
        return redirect('orders:checkout')
    
    if request.method == 'POST':
        # Obtener datos del formulario de pago
        payment_method = request.POST.get('payment_method', 'card')
        card_number = request.POST.get('card_number', '').replace(' ', '')
        card_name = request.POST.get('card_name', '').strip()
        expiry_date = request.POST.get('expiry_date', '').strip()
        cvv = request.POST.get('cvv', '').strip()
        
        # Validaciones básicas (ilustrativas)
        errors = []
        
        if payment_method == 'card':
            if not card_number or len(card_number) < 13 or len(card_number) > 19:
                errors.append("Número de tarjeta inválido. Debe tener entre 13 y 19 dígitos.")
            
            if not card_name or len(card_name) < 3:
                errors.append("El nombre en la tarjeta es requerido.")
            
            if not expiry_date or len(expiry_date) != 5:
                errors.append("Fecha de expiración inválida. Formato: MM/AA")
            
            if not cvv or len(cvv) < 3 or len(cvv) > 4:
                errors.append("CVV inválido. Debe tener 3 o 4 dígitos.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            cart_items = cart.items.all()
            context = {
                'cart': cart,
                'cart_items': cart_items,
                'shipping_address': shipping_address,
                'total_items': cart.get_total_items(),
                'total_price': cart.get_total_price(),
                'form_data': {
                    'payment_method': payment_method,
                    'card_name': card_name,
                    'expiry_date': expiry_date,
                }
            }
            return render(request, 'orders/payment.html', context)
        
        # Crear la orden
        order = Order.objects.create(
            user=request.user,
            status='paid',
            shipping_address=shipping_address
        )
        
        # Crear los items de la orden y actualizar stock
        for cart_item in cart.items.all():
            # Verificar stock disponible
            if cart_item.product.stock < cart_item.quantity:
                messages.error(request, f"Stock insuficiente para {cart_item.product.name}")
                order.delete()
                return redirect('orders:cart')
            
            # Crear item de la orden
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
            
            # Actualizar stock del producto
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Limpiar el carrito
        cart.items.all().delete()
        
        # Limpiar la sesión
        if 'selected_shipping_address' in request.session:
            del request.session['selected_shipping_address']
        
        messages.success(request, f"¡Pago procesado exitosamente! Orden #{order.id} creada.")
        return redirect('orders:order_confirmation', order_id=order.id)
    
    cart_items = cart.items.all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'shipping_address': shipping_address,
        'total_items': cart.get_total_items(),
        'total_price': cart.get_total_price(),
    }
    
    return render(request, 'orders/payment.html', context)


@login_required
def order_confirmation_view(request, order_id):
    """Vista para mostrar la confirmación de la orden"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all(),
        'total_amount': sum(item.get_total() for item in order.items.all()),
    }
    
    return render(request, 'orders/order_confirmation.html', context)


@login_required
def order_history_view(request):
    """Vista para mostrar el historial de órdenes del usuario"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_history.html', context)


@login_required
@require_POST
def cancel_order(request, order_id):
    """Vista para cancelar una orden"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Solo se pueden cancelar órdenes que estén en estado 'pending' o 'paid'
    if order.status not in ['pending', 'paid']:
        messages.error(request, f"No se puede cancelar la orden #{order.id}. Estado actual: {order.get_status_display()}")
        return redirect('orders:order_history')
    
    # Restaurar el stock de los productos
    for item in order.items.all():
        if item.product:  # Verificar que el producto aún exista
            item.product.stock += item.quantity
            item.product.save()
    
    # Cambiar el estado de la orden a cancelada
    order.status = 'cancelled'
    order.save()
    
    messages.success(request, f"La orden #{order.id} ha sido cancelada exitosamente. El stock de los productos ha sido restaurado.")
    
    # Redirigir de vuelta a donde estaba el usuario
    return redirect(request.META.get('HTTP_REFERER', 'orders:order_history'))
