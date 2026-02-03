import datetime
import json
from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order, Payment




def payments(request):
    body=json.loads(request.body)
    # print('BODY:',body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    
    # store transaction detail in payment model
    payment=Payment(user=request.user,
                    payment_id=body['transactionID'],
                    payment_method=body['paymentMethod'],
                    amount_paid=order.order_total,
                    status=body['status'],
                    )
    payment.save()

    order.payment=payment   
    order.is_ordered=True
    order.save()

    return render(request,'orders/payments.html')
# Create your views here.
def place_order(request,total=0,quantity=0,):
    current_user=request.user
    # check the cart count if it is less than or equal to 1 redirect ot shop
    cart_items=CartItem.objects.filter(user=current_user)
    cart_count=cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    grand_total=0
    tax=0
    for cart_item in cart_items:
        total +=(cart_item.product.price * cart_item.quantity)
        quantity +=cart_item.quantity
    tax=(2*total)/100
    grand_total=total+tax
    
    if request.method=='POST':
        form=OrderForm(request.POST)

        # print("FORM VALID:", form.is_valid())


        if form.is_valid():
            #store all the billing information inside the tbale 
            data=Order()
            data.user=current_user
            #get the filed value from the form and assign to order model table
            data.f_name=form.cleaned_data['f_name']
            data.l_name=form.cleaned_data['l_name']
            data.phone=form.cleaned_data['phone']
            data.email=form.cleaned_data['email']
            data.address_line1=form.cleaned_data['address_line1']
            data.address_line2=form.cleaned_data['address_line2']
            data.country=form.cleaned_data['country']
            data.state=form.cleaned_data['state']
            data.city=form.cleaned_data['city']
            data.order_note=form.cleaned_data['order_note']
            data.order_total=grand_total
            data.tax=tax
            #to get the current  ip address of the user
            data.ip=request.META.get('REMOTE_ADDR')
            data.save()
            #generate the order number for the order 

            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
            context={
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax, 
                'grand_total':grand_total,     
            }

            return render(request,'orders/payments.html',context)
        else:
            return render(request, 'store/checkout.html', {
                'form': form,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            })
                
    else:
        return redirect('checkout')


    