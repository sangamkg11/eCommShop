from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


#custom user model

class MyAccountManager(BaseUserManager):

    def create_user(self,f_name,l_name,username,email,password=None):
        #check user have email or not if not raise the error
        if not email:
            raise ValueError("User must have an email address")
        
        #check user have an username if not then raise the error
        if not username:
            raise ValueError("User must have an username")


        user=self.model(
            #here normalize email means if we enter the email into the capital letter then it make into thesmall letter
            email=self.normalize_email(email),
            username=username,
            f_name=f_name,
            l_name=l_name,
        )

        #not set the password as password

        user.set_password(password)
        user.save(using=self._db)
        return user
    

    #write the function to create the super user

    def create_superuser(self,f_name,l_name,email,username,password):
        #we create the superuser with the help of method of create_user
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            f_name=f_name,
            l_name=l_name,

        )
        #now give all the permision
        user.is_admin=True
        user.is_staff=True
        user.is_active=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    f_name=models.CharField(max_length=50)
    l_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_no=models.CharField(max_length=50)

    #some required field for the custome login field

    date_join=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    #to use email for the login 
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','f_name','l_name']

    objects=MyAccountManager()

    def __str__(self):
        return self.username+","+self.email
    
    def full_name(self):
        return f'{self.f_name} {self.l_name}'
    
    #mandatory this to use for the custom user model

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,add_label):
        return True
