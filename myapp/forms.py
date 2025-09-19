# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
# from .models import Product

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(required=False)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')

# class BootstrapLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for _, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['title', 'category', 'name', 'description', 'price', 'image', 'location']

#         widgets = {
#             'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
#             'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Product

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class BootstrapLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'category', 'name', 'description', 'price', 'image', 'location']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# ✅ new form
class ContactSellerForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'border p-2 rounded-lg'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'border p-2 rounded-lg'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'border p-2 rounded-lg'}))
