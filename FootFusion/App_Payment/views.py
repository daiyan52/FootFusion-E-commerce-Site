from django.shortcuts import render, redirect
from .forms import billingAddressForm
from .models import billingAddress
from App_Order.models import Order
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import HttpResponse

def checkoutView(request):
    saved_address, created = billingAddress.objects.get_or_create(user=request.user)
    form = billingAddressForm(instance=saved_address)
    
    if request.method == 'POST':
        form = billingAddressForm(request.POST, instance=saved_address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address Saved")
            return redirect('App_Payment:payment')
    
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_total = order_qs[0].get_totals()
    
    return render(request, 'App_Payment/checkOut.html', {
        'form': form,
        'order_items': order_items, 
        'order_total': order_total,
        'saved_address': saved_address,
    })


def paymentView(request):
    saved_address = billingAddress.objects.get_or_create(user=request.user)[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if not order_qs.exists():
        # Handle the case where no active order exists for the user
        messages.error(request, "No active order found.")
        return redirect('App_Payment:checkout')
    
    order = order_qs[0]
    amount = int(order.get_totals() * 100)  # Convert amount to paisa

    try:
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1,  # Capture payment automatically
        }
        razorpay_order = razorpay_client.order.create(data=payment_data)
        razorpay_order_id = razorpay_order['id']
        payment_data['receipt'] = 'order_rcptid_' + str(order.id)
    except razorpay.errors.BadRequestError as e:
        # Handle specific Razorpay API errors
        messages.error(request, "Razorpay API Error: {}".format(e))
        return redirect('App_Payment:payment')
    except Exception as e:
        # Handle other exceptions
        messages.error(request, "Failed to create Razorpay order: {}".format(e))
        return redirect('App_Payment:payment')
    
    return render(request, 'App_Payment/pay.html', {
        'razorpay_key': settings.RAZORPAY_API_KEY,
        'amount': amount,
        'razorpay_order_id': razorpay_order_id,
        'order': order,
        'saved_address': saved_address,
    })
# @csrf_exempt

def paymentSuccess(request):
    if request.method == 'POST' or request.method == 'GET':
        payment_data = request.POST
        print(payment_data)
        return render(request, 'App_Payment/success.html')
    else:
        return HttpResponse(status=405)
