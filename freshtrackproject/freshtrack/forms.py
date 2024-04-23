from django import forms
from .models import User

class RegistrationForm(forms.ModelForm):
    # Definisci il campo email nel form
    email = forms.EmailField(label='Email')

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'password']

    def clean_email(self):
        # Ottieni l'email inserita dall'utente
        email = self.cleaned_data.get('email')
        # Verifica se esiste già un utente con la stessa email nel database
        if User.objects.filter(email=email).exists():
            # Aggiungi un messaggio di errore al campo email
            self.add_error('email', "This email has already been used.")
        return email
