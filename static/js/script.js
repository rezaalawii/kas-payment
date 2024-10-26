// Inisialisasi Xendit
Xendit.setPublishableKey(document.getElementById('xendit-key').dataset.key);

document.getElementById('payment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Tampilkan loading state
    const submitButton = this.querySelector('button[type="submit"]');
    const originalText = submitButton.innerText;
    submitButton.disabled = true;
    submitButton.innerText = 'Memproses...';
    
    const formData = {
        nama: document.getElementById('nama').value,
        bulan: document.getElementById('bulan').value,
        jumlah: document.getElementById('jumlah').value,
        payment_method: document.querySelector('input[name="payment_method"]:checked').value
    };

    // Kirim ke backend
    fetch('/api/create-payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.payment_url) {
            window.location.href = data.payment_url;
        } else {
            throw new Error(data.message || 'Terjadi kesalahan');
        }
    })
    .catch(error => {
        alert('Error: ' + error.message);
        submitButton.disabled = false;
        submitButton.innerText = originalText;
    });
});

// Validasi form
document.querySelectorAll('#payment-form input[required], #payment-form select[required]').forEach(input => {
    input.addEventListener('invalid', (e) => {
        e.preventDefault();
        input.classList.add('border-red-500');
    });
    
    input.addEventListener('input', () => {
        input.classList.remove('border-red-500');
    });
});