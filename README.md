PayHero Flask M-Pesa Integration

A clean Flask application that integrates PayHero M-Pesa STK Push, stores transactions in SQLite, handles callbacks, and supports payment reconciliation.

Features

M-Pesa STK Push via PayHero API

Strict Kenyan phone number validation (2547XXXXXXXX / 2541XXXXXXXX)

SQLite database for transaction tracking

Callback handling with detailed status mapping

Payment reconciliation endpoint

Callback logging for debugging & auditing

Environment-based configuration (.env)

Project Structure
payhero_flask_mpesa/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env
└── templates/
    └── index.html

Requirements

Python 3.8+

PayHero API credentials

Internet access (for PayHero requests)

Installation
1. Clone the repository
git clone https://github.com/yourusername/payhero_flask_mpesa.git
cd payhero_flask_mpesa

2. Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

Environment Configuration

Create a .env file in the project root:

SECRET_KEY=dev_secret_key
DATABASE=transactions.db

PAYHERO_BASE_URL=https://backend.payhero.co.ke/api/v2
PAYHERO_CHANNEL_ID=your_channel_id
PAYHERO_PROVIDER=m-pesa

API_USERNAME=your_payhero_api_username
API_PASSWORD=your_payhero_api_password

CALLBACK_URL=https://your_domain.com/callback

⚠️ Important Notes

CALLBACK_URL must be publicly accessible (use Ngrok during development)

Never commit .env to version control

Credentials must match your PayHero dashboard

Running the Application
python app.py


The app will start on:

http://localhost:7000


On startup:

SQLite database (transactions.db) is auto-created

payments table is initialized automatically

Endpoints Overview
/ – Payment Page

Displays the HTML payment form.

/pay – Initiate M-Pesa STK Push

Method: POST

Form Fields:

amount – Minimum KES 1

phone_number – Format: 2547XXXXXXXX

external_reference – Exactly 8 characters, unique

Example Response (Success):

{
  "success": true,
  "message": "M-Pesa STK initiated successfully! Check your phone.",
  "reference": "ABCD1234",
  "payhero_reference": "PHR-XXXX"
}

/callback – PayHero Callback Endpoint

Method: POST or GET

Handles:

Successful payments

Failures

User cancellations

Timeouts

Automatically:

Updates transaction status

Logs callbacks to callback_logs.json

/reconcile/<reference> – Recheck Payment Status

Method: GET

Used when:

Callback delays occur

Network issues happen

Manual verification is needed

Returns:

Local DB status

Remote PayHero status (if available)

Payment Status Mapping
Result Code	Status	Description
0	completed	Payment successful
1	failed	General failure
1031	cancelled	User cancelled
1032	cancelled	User cancelled
1037	timeout	Request timeout
Others	failed	API / system error
Database Schema

Table: payments

Column	Type	Description
id	INTEGER	Primary key
phone	TEXT	Customer phone number
amount	REAL	Payment amount
reference	TEXT	Unique external reference
status	TEXT	pending / completed / failed
reason	TEXT	Status explanation
timestamp	DATETIME	Created time
updated_at	DATETIME	Last update
Callback Logs

All callbacks are stored in:

callback_logs.json


Keeps last 1000 entries

Useful for debugging PayHero issues

Safe to rotate or delete

Security Notes (Important)

Use HTTPS in production

Disable debug=True in production

Validate callback IPs if PayHero provides them

Store secrets in environment variables only

Development Tips

Use Ngrok for local callback testing

Always verify external_reference uniqueness

Monitor callback logs during live payments

Use /reconcile if callbacks fail

License

MIT License — free to use, modify, and distribute.

Author

Built with ❤️ using Flask & PayHero M-Pesa API.
