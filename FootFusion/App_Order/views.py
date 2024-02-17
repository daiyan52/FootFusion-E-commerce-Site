from django.shortcuts import render, get_object_or_404, redirect
from App_Order.models import Order, Cart
from App_shop.models import Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_item, created = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.orderitems.filter(item=item).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f' Cart Item {item.name} updated successfully')
            return redirect('App_shop:home')

        else:
            order.orderitems.add(order_item)
            messages.success(request, f'Item {item.name} added to cart successfully')
            return redirect('App_shop:home')

    else:
        order = Order.objects.create(user=request.user)
        order.orderitems.add(order_item)
        messages.success(request, f'Item {item.name} added to cart successfully')
        return redirect('App_shop:home')

@login_required

def cart_view(request):
    carts = Cart.objects.filter(user=request.user,purchased=False)
    orders = Order.objects.filter(user=request.user,ordered=False)

    if carts.exists() and orders.exists():
        orders = orders[0]
        return render(request,'App_Order/cart.html',{'orders':orders,'carts':carts})