🚀 PayHero Flask M-Pesa Integration

A clean Flask + PayHero integration for M-Pesa STK Push, with callbacks, reconciliation, and SQLite persistence.

<p align="center"> <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" /> <img src="https://img.shields.io/badge/M--Pesa-Payments-green?style=for-the-badge" /> <img src="https://img.shields.io/badge/SQLite-Database-blue?style=for-the-badge" /> </p>
✨ What This Project Does

✅ Initiates M-Pesa STK Push via PayHero
✅ Validates Kenyan phone numbers strictly (2547… / 2541…)
✅ Stores transactions safely in SQLite
✅ Handles PayHero callbacks correctly
✅ Supports manual payment reconciliation
✅ Logs callbacks for debugging & audits

Built to survive real-world failures (timeouts, retries, missing callbacks).

📂 Project Structure
payhero_flask_mpesa/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env
└── templates/
    └── index.html

🧰 Tech Stack
Tool	Purpose
Flask	Backend API
SQLite	Local database
PayHero API	M-Pesa STK Push
Python Dotenv	Environment variables
Requests	HTTP calls
⚙️ Installation
1️⃣ Clone the repo
git clone https://github.com/yourusername/payhero_flask_mpesa.git
cd payhero_flask_mpesa

2️⃣ Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate

3️⃣ Install dependencies
pip install -r requirements.txt

🔐 Environment Setup

Create a .env file in the project root:

SECRET_KEY=dev_secret_key
DATABASE=transactions.db

PAYHERO_BASE_URL=https://backend.payhero.co.ke/api/v2
PAYHERO_CHANNEL_ID=your_channel_id
PAYHERO_PROVIDER=m-pesa

API_USERNAME=your_payhero_api_username
API_PASSWORD=your_payhero_api_password

CALLBACK_URL=https://your_domain.com/callback

⚠️ Important

CALLBACK_URL must be public

Use Ngrok during development

Never commit .env

▶️ Running the App
python app.py


App runs on:

http://localhost:7000


🧠 On startup:

Database is auto-created

Payments table is initialized

No manual migration needed

🌍 API Endpoints
🏠 /

Displays the payment form.

💳 /pay — Initiate STK Push

Method: POST

Required Fields

amount (≥ 1 KES)

phone_number → 2547XXXXXXXX

external_reference → 8 characters

✅ Success Response

{
  "success": true,
  "message": "M-Pesa STK initiated successfully!",
  "reference": "ABCD1234"
}

🔔 /callback — PayHero Webhook

Method: POST / GET

Handles:

✔ Success

❌ Failure

⏱ Timeout

🚫 User cancellation

Automatically updates DB & logs data.

🔁 /reconcile/<reference>

Method: GET

Used when:

Callback delays occur

Network interruptions happen

Manual verification is required

Returns:

Local DB status

Remote PayHero status

📊 Payment Status Mapping
Result Code	Status
0	✅ Completed
1	❌ Failed
1031	🚫 Cancelled
1032	🚫 Cancelled
1037	⏱ Timeout
Others	❌ Failed
🗄 Database Schema
payments Table
Column	Description
phone	Customer number
amount	Amount paid
reference	Unique ID
status	Payment state
reason	Status message
timestamp	Created time
updated_at	Last update
📝 Callback Logs

Stored in:

callback_logs.json


Keeps last 1000 callbacks

Perfect for debugging PayHero issues

🔒 Security Tips

🔐 Use HTTPS in production
🚫 Disable debug=True
🛡 Validate webhook source IPs
🧾 Never log credentials

🧪 Dev Tips

💡 Use Ngrok for callbacks
💡 Always reconcile stuck payments
💡 Monitor callback logs
💡 Handle retries gracefully

📄 License

MIT — free to use, modify, and ship.

👨🏽‍💻 Author

Built with Flask, caffeine ☕ and real-world payment pain.
