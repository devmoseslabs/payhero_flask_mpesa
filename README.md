# PayHero Flask M-Pesa Integration

A Flask application for integrating **PayHero M-Pesa STK Push** with callback handling, transaction storage, and reconciliation.

---

## Features

- M-Pesa STK Push via PayHero API
- Strict Kenyan phone number validation (2547XXXXXXXX / 2541XXXXXXXX)
- SQLite database for transaction tracking
- Reliable callback processing
- Manual payment reconciliation endpoint
- Callback logging for audits and debugging
- Environment-based configuration

---

## Project Structure

payhero_flask_mpesa/
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── .env
└── templates/
└── index.html

yaml
Copy code

---

## Requirements

- Python 3.8+
- PayHero API credentials
- Internet access

---

## Installation

### Clone the repository
git clone https://github.com/yourusername/payhero_flask_mpesa.git
cd payhero_flask_mpesa

graphql
Copy code

### Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

shell
Copy code

### Install dependencies
pip install -r requirements.txt

yaml
Copy code

---

## Environment Configuration

Create a `.env` file in the project root:

SECRET_KEY=dev_secret_key
DATABASE=transactions.db

PAYHERO_BASE_URL=https://backend.payhero.co.ke/api/v2
PAYHERO_CHANNEL_ID=your_channel_id
PAYHERO_PROVIDER=m-pesa

API_USERNAME=your_payhero_api_username
API_PASSWORD=your_payhero_api_password

CALLBACK_URL=https://your_domain.com/callback

yaml
Copy code

### Notes
- `CALLBACK_URL` must be publicly accessible
- Use Ngrok during development
- Do not commit `.env` to GitHub

---

## Running the Application

python app.py

nginx
Copy code

The app runs on:

http://localhost:7000

yaml
Copy code

On startup:
- SQLite database is created automatically
- Payments table is initialized

---

## API Endpoints

### `/`
Displays the payment page.

### `/pay` (POST)
Initiates M-Pesa STK Push.

Required fields:
- amount (minimum 1 KES)
- phone_number (2547XXXXXXXX)
- external_reference (exactly 8 characters)

### `/callback` (POST / GET)
Handles PayHero payment callbacks and updates transaction status.

### `/reconcile/<reference>` (GET)
Re-checks payment status from PayHero and updates local records.

---

## Payment Status Mapping

| Result Code | Status     |
|------------|------------|
| 0          | completed  |
| 1          | failed     |
| 1031       | cancelled  |
| 1032       | cancelled  |
| 1037       | timeout    |
| others     | failed     |

---

## Database Schema

**payments**

| Column       | Description |
|-------------|-------------|
| phone       | Customer phone number |
| amount      | Payment amount |
| reference   | Unique reference |
| status      | Payment state |
| reason      | Status explanation |
| timestamp   | Created time |
| updated_at  | Last update |

---

## Logs

Callback logs are stored in:

callback_logs.json

yaml
Copy code

- Last 1000 callbacks are retained
- Useful for debugging and audits

---

## Security Notes

- Use HTTPS in production
- Disable debug mode
- Store secrets in environment variables only

---

## License

MIT License
