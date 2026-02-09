from django import forms
from .models import Account,UserProfile


class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password.',
        'class':'form-control',
    }))
    Confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm password.',
        
    }))
    class Meta:
        model=Account
        fields=['f_name','l_name','phone_no','email','password']

#to make the placeholder and the class in the form control for desingning the form
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)

        self.fields['f_name'].widget.attrs['placeholder']='Enter First Name'
        self.fields['l_name'].widget.attrs['placeholder']='Enter Last Name'
        self.fields['phone_no'].widget.attrs['placeholder']='Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder']='Enter Email address'

        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'

    
    #to check whether the password and the confirm password is same or not 
    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        Confirm_password=cleaned_data.get('Confirm_password')

        if password !=Confirm_password:
            raise forms.ValidationError(
                "Password & confirm password not matched !"
            )
        

    



class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['f_name','l_name','phone_no']


    def __init__(self,*args,**kwargs):
        super(UserForm,self).__init__(*args,**kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={'invalid':("Image files only")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=['address_line1','address_line2','city','state','country','profile_picture']

    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'