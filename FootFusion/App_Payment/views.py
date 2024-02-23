from django.shortcuts import render, redirect
from .forms import billingAddressForm
from .models import billingAddress
from App_Order.models import Order
from django.contrib import messages
import razorpay
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

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


# def paymentView(request):
#     saved_address = billingAddress.objects.get_or_create(user=request.user)[0]
#     order_qs = Order.objects.filter(user=request.user, ordered=False)
    
#     if not order_qs.exists():
#         # Handle the case where no active order exists for the user
#         messages.error(request, "No active order found.")
#         return redirect('App_Payment:checkout')
    
#     order = order_qs[0]
#     amount = int(order.get_totals() * 100)  # Convert amount to paisa

#     try:
#         razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
#         payment_data = {
#             'amount': amount,
#             'currency': 'INR',
#             'payment_capture': 1,  # Capture payment automatically
#         }
#         razorpay_order = razorpay_client.order.create(data=payment_data)
#         razorpay_order_id = razorpay_order['id']
#         print(razorpay_order_id)
#         payment_data['receipt'] = 'order_rcptid_' + str(order.id)
#     except razorpay.errors.BadRequestError as e:
#         # Handle specific Razorpay API errors
#         messages.error(request, "Razorpay API Error: {}".format(e))
#         return redirect('App_Payment:payment')
#     except Exception as e:
#         # Handle other exceptions
#         messages.error(request, "Failed to create Razorpay order: {}".format(e))
#         return redirect('App_Payment:payment')
    
#     return render(request, 'App_Payment/pay.html', {
#         'razorpay_key': settings.RAZORPAY_API_KEY,
#         'amount': amount,
#         'razorpay_order_id': razorpay_order_id,
#         'order': order,
#         'saved_address': saved_address,
#     })
def paymentView(request):
    saved_address = billingAddress.objects.get_or_create(user=request.user)[0]
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    if not order_qs.exists():
        # Handle the case where no active order exists for the user
        messages.error(request, "No active order found.")
        return redirect('App_Payment:checkout')
    
    order = order_qs[0]
    amount = int(order.get_totals() * 100)  # Convert amount to paisa

    if request.method == 'POST':
        form_data = request.POST
        razorpay_order_id = form_data.get('razorpay_order_id', None)
        razorpay_payment_id = form_data.get('razorpay_payment_id', None)
        razorpay_signature = form_data.get('razorpay_signature', None)
        try:
            razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            payment = razorpay_client.payment.capture(razorpay_payment_id, amount)
            transaction_id = payment['id']
            print(transaction_id)
            # Handle the transaction ID, update your Order model, etc.
        except razorpay.errors.BadRequestError as e:
            # Handle specific Razorpay API errors
            messages.error(request, "Razorpay API Error: {}".format(e))
            return redirect('App_Payment:payment')
        except Exception as e:
            # Handle other exceptions
            messages.error(request, "Failed to capture payment: {}".format(e))
            return redirect('App_Payment:payment')
        
        # Redirect to payment success page or other logic
        return redirect('App_Payment:payment_success')

    try:
        razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1,  # Capture payment automatically
        }
        razorpay_order = razorpay_client.order.create(data=payment_data)
        razorpay_order_id = razorpay_order['id']
        print(razorpay_order_id)
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

def purchase(request,transaction_id):
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    order = order_qs[0]
    order_id = transaction_id
    order.ordered = True
    order.save()

    cart_items = Order.objects.filter(user=request.user,purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('App_shop:home'))

def orderView(request):
    try:
        orders = Order.objects.filter(user=request.user,ordered=True)
        context = {'orders': orders}
    except:
        messages.warning(request,"You don't have any orders")
        return redirect('App_shop:home')
    return render(request, 'App_Payment/order.html', context)