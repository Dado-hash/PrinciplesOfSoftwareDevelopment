from django.shortcuts import redirect
from django.urls import reverse

class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path != reverse('login'):
            return redirect('login')  # Reindirizza alla pagina di login se l'utente non è autenticato e non sta cercando di accedere alla pagina di login stessa
        return self.get_response(request)
