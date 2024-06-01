document.addEventListener('DOMContentLoaded', function() {
    let isProcessingBarcode = false;  // Flag per prevenire scansioni multiple

    Quagga.init({
        inputStream: {
            name: "Live",
            type: "LiveStream",
            target: document.querySelector('#scanner-container'),  // Elemento in cui mostrare il flusso video
            constraints: {
                width: 640,
                height: 480,
                facingMode: "environment"  // Usa la fotocamera posteriore se disponibile
            }
        },
        decoder: {
            readers: ["code_128_reader", "ean_reader", "ean_8_reader", "code_39_reader", "code_39_vin_reader", "codabar_reader", "upc_reader", "upc_e_reader", "i2of5_reader"]  // Tipi di codici a barre da leggere
        }
    }, function(err) {
        if (err) {
            console.log(err);
            alert("Errore durante l'inizializzazione di QuaggaJS: " + err.message);
            return;
        }
        console.log("Initialization finished. Ready to start");
        Quagga.start();
    });

    Quagga.onDetected(function(data) {
        if (isProcessingBarcode) return;  // Se già in elaborazione, esci

        isProcessingBarcode = true;  // Imposta il flag per indicare che è in corso l'elaborazione del codice a barre
        console.log(data.codeResult.code);

        // Invia il codice a barre al server
        fetch('/add_product_barcode/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')  // Assicurati di avere il token CSRF configurato
            },
            body: JSON.stringify({ barcode: data.codeResult.code })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Product added:', data);
                // Reindirizza alla pagina home
                window.location.href = data.redirect_url;
            } else {
                console.error('Error:', data.message);
                // Gestisci l'errore
            }
        })
        .catch(error => {
            console.error('Error adding product:', error);
            // Gestisci l'errore
        })
        .finally(() => {
            isProcessingBarcode = false;  // Reimposta il flag dopo aver completato l'elaborazione
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Questo cookie inizia con il nome desiderato?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
