from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

#verification email

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


#view for the registration of new user
def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            #cleaned data is used to fetch the data from the request
            f_name=form.cleaned_data['f_name']
            l_name=form.cleaned_data['l_name']
            email=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone_no']
            password=form.cleaned_data['password']
            username=email.split("@")[0]


            user=Account.objects.create_user(f_name=f_name,l_name=l_name,email=email,username=username,password=password)

            user.phone_no=phone_no

            user.save()
            #user activation link
            current_site=get_current_site(request)
            mail_subject='Please Activate your account '
            message=render_to_string('accounts/account_varification_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()


            messages.success(request,"Thank you for connecting with us .We have sent you a verifiaction email to verify your email.Please verify it.")
            return redirect('/accounts/login?command=verification&email='+email)
    else:
        form=RegistrationForm()
    context={
        'form':form,
    }
    return render(request,'accounts/register.html',context)



#views for the login to the existing user 
def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        user=auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            # messages.success(request,"You are logged in!!")
            return redirect('home')
        else:
            messages.error(request,"Invalid login credentials")
            return redirect('login')



    return render(request,'accounts/login.html')




#views for the logout the user means delte the session is and key 
def logout(request):
    

    return 


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None 


    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,"Account activate successfully")
        return redirect('login')
    
    else:
        messages.error(request,'Invalis activation link')
        return redirect('register')

    