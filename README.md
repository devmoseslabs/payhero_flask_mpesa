# Mini Pesa – Simple M-Pesa STK Push App

Mini Pesa is a lightweight Flask application that allows you to initiate M-Pesa STK push payments, handle callbacks, and reconcile payment status. This project is designed as a simple foundation for building payment-enabled applications.

---

## Features
- Initiate M-Pesa STK push payments via PayHero API
- Validate phone numbers and amounts
- Handle PayHero callbacks automatically
- Log callback data for review
- Reconcile payment status with remote API
- Lightweight SQLite database for storage

---

## Setup

1. **Copy `env.example` to `.env`**  
cp env.example .env

makefile
Copy code
Or create a `.env` file manually and fill in your own credentials.

2. **Fill in environment variables in `.env`**  
Example:
```text
SECRET_KEY=your-secret-key
API_USERNAME=your-api-username
API_PASSWORD=your-api-password
CALLBACK_URL=https://yourdomain.com/callback
CHANNEL_ID=1959
Install dependencies

nginx
Copy code
pip install -r requirements.txt
Run the app

nginx
Copy code
python app.py
Open the payment page
Go to http://localhost:7000 in your browser.

Notes
Ensure CALLBACK_URL is publicly accessible for PayHero to send updates.

Do not upload your .env, transactions.db, or callback_logs.json to GitHub.

The default CHANNEL_ID is 1959 (change if required).

SQLite database (transactions.db) stores payment records locally.

Project Structure
bash
Copy code
mini_pesa/
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
├── templates/
│   └── payment.html       # Payment page template
├── env.example            # Sample environment variables
└── README.md              # Project instructions
Future Improvements
Async callback handling for higher traffic

Replace JSON log with database or logging system

Multi-provider support for payments

Mask sensitive data in logs for security
