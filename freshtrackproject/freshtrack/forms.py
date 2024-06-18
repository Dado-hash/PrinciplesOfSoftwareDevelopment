from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from freshtrack.models import Profile, ShoppingList, Product


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ShoppingListForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['product_name', 'quantity', 'unit_of_measure', 'always_in_stock']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'quantity', 'unit_of_measure', 'expiration_date', 'always_in_stock']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}),  # Aggiungi un placeholder per la data
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['expiration_date'].required = False  # Imposta il campo expiration_date come non obbligatorio


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'expiration_date', 'category', 'storage_location', 'status', 'quantity', 'unit_of_measure', 'always_in_stock', 'notes']

class UploadReceiptForm(forms.Form):
    receipt_image = forms.ImageField()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'profile_picture']
