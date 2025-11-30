## ◇────── PAYHERO_FLASK_MPESA ───────◇

ㅤ
<p align="center">
  <a href="" rel="noopener">
    <img width="300px" height="300px" src="https://your-image-host.com/logo.png" alt="Mini Pesa Logo">
  </a>
</p>

![Python](https://img.shields.io/badge/Python-3.7+-blue) ![Flask](https://img.shields.io/badge/Flask-Framework-orange) ![M-Pesa](https://img.shields.io/badge/M--Pesa-PayHero-green) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 🌟 Features

- 💸 Initiate **M-Pesa STK Push** payments  
- 🖥️ Single-page **responsive interface**  
- 🔄 **Callback handling** and real-time status updates  
- 📊 Track all payment attempts in a **local database**  
- ⚡ Lightweight and easy to configure  

---

## 🚀 Installation & Setup

### 1️⃣ Environment Variables

Create a `.env` file in your project root:

```env
SECRET_KEY=your-secret-key
API_USERNAME=your-payhero-username
API_PASSWORD=your-payhero-password
CALLBACK_URL=https://your-domain.com/callback
CHANNEL_ID=1959
Use env.example as a template.

2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the App
bash
Copy code
python app.py
Open http://localhost:7000 in your browser.

📷 Screenshots
<details> <summary><b>Click to view the payment page</b></summary> <br/> <p align="center"> <img src="https://your-image-host.com/payment_page.png" width="400px"> </p> </details> <details> <summary><b>Click to view callback logs</b></summary> <br/> <p align="center"> <img src="https://your-image-host.com/callback_logs.png" width="400px"> </p> </details>
🔗 API Endpoints
Endpoint	Method	Description
/	GET	Serve payment page
/pay	POST	Initiate payment
/callback	POST	Handle payment callbacks
/reconcile/<reference>	GET	Check payment status

📁 Project Structure
bash
Copy code
mini_pesa/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── payment.html       # Single-page payment interface
├── env.example            # Template for environment variables
├── transactions.db        # SQLite database (auto-created)
└── callback_logs.json     # Callback logs (auto-created)
⚠️ Notes
Ensure CALLBACK_URL is publicly accessible.

Do not commit .env, transactions.db, or callback_logs.json.

Payment PINs are never stored.

Default CHANNEL_ID is 1959 (change if needed).

📞 Support & Contact
🐦 Telegram: @DevMoses

🌐 Portfolio: devmoses.online

📄 License

Built with ❤️ by DevMoses
