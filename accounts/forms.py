from django import forms
from .models import Account


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