import time
from django.http import JsonResponse

def hello(request):
    # Verifica se è stata fornita una query nella richiesta
    name = request.GET.get('name')
    if name:
        # Costruisci un dizionario di risposta
        response = {
            'message': f'Hello, {name}!',
            'timestamp': int(time.time())
        }
        # Restituisci la risposta come JSON
        return JsonResponse(response)
    else:
        # Se il parametro 'name' non è fornito, restituisci un messaggio di errore
        return JsonResponse({'error': 'Parametro "name" mancante'})
