from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
# from django.urls import reverse
from carts.models import Cart, CartItem
from store.models import Product, Variation
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# undescore before the the function name is use to make them as private function
#and it store the session key  for the cart if they are added or not

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

# add cart logic 
def add_cart(request,product_id):
    product=Product.objects.get(id=product_id) #get the product
    # variation=None
    product_variation=[]
    if request.method == 'POST':
        for item in request.POST:
            key=item
            value=request.POST[key]
            # print(key,value)
            
            # getting the variation
            try:
                variation=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                # print(variation)
                product_variation.append(variation)

            except:
                pass
    
    # cart=None
    #getting the cart here
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))    #get the cart using the cart_id present in the session

    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    #getting the cartitems here 
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        #getting the variation in the cart
        if len(product_variation)>0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)


        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        if len(product_variation)>0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()
    #this line is use to check  when we add the product in cart it will go or not

    # return HttpResponse(cart_item.product)
    # exit()

    
    return redirect('cart')

    # this redirect('cart') is not working thats why we use this below line
    # return redirect(f"{reverse('cart')}?added={product_id}")



#method to remove decrease the quantity

def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(cart=cart,product=product)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')


def del_cart_item(request,product_id):
    
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    
    cart_item.delete()
    return redirect('cart')

    


#cart page 
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for cart_item in cart_items:
            total +=(cart_item.product.price * cart_item.quantity)
            quantity +=cart_item.quantity
        tax=(2*total)/100
        grand_total=total+tax
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'tax':tax,
        'grand_total':grand_total,
    }

    return render(request,'store/cart.html',context)