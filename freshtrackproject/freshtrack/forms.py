from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from freshtrack.models import Profile, ShoppingList, Product
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email has already been used.")
        return email

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

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', strip=False, widget=forms.PasswordInput)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                'This account is inactive.',
                code='inactive',
            )
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("The username does not exist.")
        return username
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    'The username does not exist.',
                    code='invalid_login',
                )

            if not user.check_password(password):
                raise forms.ValidationError(
                    'Incorrect password.',
                    code='invalid_login',
                )
        
        return self.cleaned_data
