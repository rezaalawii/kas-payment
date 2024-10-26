from flask import Flask, render_template, request, jsonify
from xendit import Xendit
from dotenv import load_dotenv
import os
import uuid

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')

# Inisialisasi Xendit
xendit_client = Xendit(api_key=os.getenv('XENDIT_SECRET_KEY'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/create-payment', methods=['POST'])
def create_payment():
    try:
        data = request.json
        
        # Generate unique ID untuk external_id
        unique_id = str(uuid.uuid4())[:8]
        
        # Buat invoice menggunakan Xendit
        invoice = xendit_client.Invoice.create(
            external_id=f"KAS-{unique_id}-{data['bulan']}",
            amount=int(data['jumlah']),  # Sekarang 30000
            payer_email="",
            description=f"Pembayaran Kas Kelas - {data['bulan'].title()}",
            customer={
                "given_names": data['nama'],
                "email": "",
            },
            items=[
                {
                    "name": f"Kas Kelas Bulan {data['bulan'].title()}",
                    "quantity": 1,
                    "price": int(data['jumlah']),  # Sekarang 30000
                    "category": "Kas Kelas",
                }
            ],
            payment_methods=[data['payment_method']]
        )
        
        return jsonify({
            "status": "success",
            "payment_url": invoice.invoice_url
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)