# Mini Pesa – Simple M-Pesa STK Push App

![Python](https://img.shields.io/badge/Python-3.7+-yellow) ![Flask](https://img.shields.io/badge/Framework-Flask-blue) ![PayHero](https://img.shields.io/badge/PayHero-API-green)

A lightweight Flask app to initiate **M-Pesa STK push payments**, handle callbacks, and track payment status in a local database.

---

## 🌟 Features

- 🖥️ **Single-page interface** – Modern and responsive form  
- 💸 **M-Pesa STK Push** – Initiate payments directly to users’ phones  
- 🔄 **Callback handling** – Automatic status updates  
- 📊 **Database logging** – Store all payment attempts locally  
- ⚡ **Lightweight & simple** – Easy setup and integration  

---

## 🚀 Setup

### 1️⃣ Environment Variables

Create a `.env` file (do **not** upload this file):

```env
SECRET_KEY=your-secret-key
API_USERNAME=your-api-username
API_PASSWORD=your-api-password
CALLBACK_URL=https://your-domain.com/callback
CHANNEL_ID=1959
Use env.example as a template.

2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run the Application
bash
Copy code
python app.py
Open http://localhost:7000 in your browser.

📝 Usage
Fill Amount, Phone Number, and Reference.

Click Initiate M-Pesa Payment.

Complete payment on your phone.

Watch real-time status updates on the web page.

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
│   └── payment.html       # Payment page template
├── env.example            # Template for environment variables
├── README.md              # Project instructions
├── transactions.db        # SQLite database (auto-created)
└── callback_logs.json     # Callback logs (auto-created)
⚠️ Notes
Ensure CALLBACK_URL is publicly accessible.

Do not commit .env, transactions.db, or callback_logs.json.

Payment PINs are never stored.

Default CHANNEL_ID is 1959 (change if needed).

Built with ❤️ by DevMoses
