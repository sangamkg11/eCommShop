
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from carts.models import CartItem
from carts.views import _cart_id
from category.models import Category
from orders.models import OrderProduct
from .models import Product, ProductGallery
from django.db.models import Q
from .models import ReviewRating
from .forms import ReviewForm


# for pahinator
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

# Create your views here.
def store(request,category_slug=None):
    #search by category
    categories=None
    products=None
    if category_slug!=None:
        categories=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.filter(category=categories,is_available=True)
        #paginator for categories products
        paginator=Paginator(products,6)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)
        products_count=products.count()
    else:


        products=Product.objects.all().filter(is_available=True).order_by('id')
        #paginator concept using start from here after fethcing the data from product
        paginator=Paginator(products,6)
        page=request.GET.get('page')
        paged_product=paginator.get_page(page)

        products_count=products.count()
    context={
        'products':paged_product,
        'products_count':products_count,

    }
    return render(request,'store/store.html',context)



def product_details(request,category_slug,product_slug):
    try:
        # __ is a syatnaxx to acees the slug value of thatr models 
        # this is write to get the single product from the page
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()    #here __ is used to get the data from cart which is usedd as a foreign key
        #the in_cart value give you the boolean value that it conatin the itms in the cart or not 
        
    except Exception as e:

        raise e
    

    if request.user.is_authenticated:

        try:
            order_product=OrderProduct.objects.filter(user=request.user,product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product=None

    else:
        order_product=None

    reviews=ReviewRating.objects.filter(product_id=single_product.id,status=True)


    #get the product gallery images

    product_gallery=ProductGallery.objects.filter(product_id=single_product.id)
    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'order_product':order_product,
        'reviews':reviews,
        'product_gallery':product_gallery,

    }
    return render(request,'store/product_details.html',context)



def search(request):
    products_count=0
    products = Product.objects.none() 
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_at').filter(Q(product_description__icontains=keyword) | Q(product_name__icontains=keyword)) 
            #here we use this Q for make the implimatation of the or opertor like if it match any one of this 2 condtion then it return tru
            #__icontains search for the whole content in description as well as its related content also
            products_count=products.count()
    context={
        'products':products,
        # 'products_count':products.count(),
        'products_count':products_count,
    }

    return render(request,'store/store.html',context)



def submit_review(request,product_id):

    url=request.META.get('HTTP_REFERER') #this is used to get the url of the page from which we are coming to this view and after submiting the review we will redirect to that page only
    if request.method=='POST':
        try:
            reviews=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=reviews)  #here we use the instance to update the review if it is already exist in the database
            form.save()
            messages.success(request,'Thank you your review has been updated successfully')
            return redirect(url)

        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            if form.is_valid():
                data=ReviewRating()
                data.subject=form.cleaned_data['subject']
                data.review=form.cleaned_data['review']
                data.rating=form.cleaned_data['rating']
                data.ip=request.META.get('REMOTE_ADDR')
                data.product_id=product_id
                data.user_id=request.user.id
                data.save()
                messages.success(request,'Thank you your review has been submitted successfully')
                return redirect(url)




        
