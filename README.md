
```markdown
# M-Pesa Payment Gateway

A simple, single-page Flask application for processing M-Pesa payments via STK Push. This project provides a clean interface to initiate M-Pesa payments and handle callbacks from the PayHero API.

![M-Pesa Payment](https://img.shields.io/badge/Payment-M--Pesa-green) ![Flask](https://img.shields.io/badge/Framework-Flask-blue) ![Python](https://img.shields.io/badge/Language-Python-yellow)

## 🌟 Features

- **Single Page Interface** - Clean, modern payment form
- **M-Pesa STK Push** - Direct integration with M-Pesa
- **Real-time Status Updates** - Live payment status polling
- **Callback Handling** - Automatic payment confirmation
- **Database Logging** - Track all payment attempts
- **Responsive Design** - Works on desktop and mobile

## 🚀 How It Works

### Architecture Flow

```

User Input → Flask App → PayHero API → M-Pesa → User's Phone → Callback → Database

````

### Detailed Process

1. **User Initiates Payment**
   - User fills amount, phone number, and reference
   - Form submits to `/pay` endpoint via AJAX

2. **STK Push Initiation**
   - Flask app sends request to PayHero API with payment details
   - PayHero triggers M-Pesa STK push to user's phone

3. **User Completes Payment**
   - User receives M-Pesa prompt on their phone
   - User enters M-Pesa PIN to authorize payment

4. **Callback Processing**
   - M-Pesa sends payment result to `/callback` endpoint
   - Application updates payment status in database

5. **Status Monitoring**
   - Frontend polls `/reconcile/{reference}` every few seconds
   - Real-time status updates displayed to user

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7+
- M-Pesa PayHero account credentials
- Ngrok or similar tunneling service for callbacks

### 1. Prepare Environment Variables

Create a `.env` file in the project root (never commit this file!):

```env
SECRET_KEY=your-secret-key
API_USERNAME=your-api-username
API_PASSWORD=your-api-password
CALLBACK_URL=https://your-domain.com/callback
CHANNEL_ID=get_from_your_payhero_dashboard
````

> You can use `env.example` as a template.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

Access the payment page at `http://localhost:7000`.

### 4. Set Up Ngrok (for callbacks)

```bash
ngrok http 7000
```

Update your `.env` `CALLBACK_URL` with the ngrok URL.

---

## 📋 Usage Guide

### For End Users

1. Open `http://localhost:7000` in your browser
2. Fill payment details:

   * **Amount**: Minimum 1 KES
   * **Phone Number**: Registered M-Pesa number (07XXXXXXXX or 2547XXXXXXXX)
   * **Reference**: Payment description
3. Click **Initiate M-Pesa Payment**
4. Complete payment on your phone
5. Watch real-time status updates on the page

### For Developers

#### API Endpoints

* `GET /` - Serve payment page
* `POST /pay` - Process payment request
* `POST /callback` - Handle PayHero callbacks
* `GET /reconcile/<reference>` - Check payment status

#### Database Schema

```sql
CREATE TABLE payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL,
    amount REAL NOT NULL,
    reference TEXT NOT NULL UNIQUE,
    status TEXT DEFAULT 'pending',
    reason TEXT DEFAULT '',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔧 Notes

* Ensure `CALLBACK_URL` is publicly accessible
* Default `CHANNEL_ID` is 1959
* Do **not** commit `.env`, `transactions.db`, or `callback_logs.json` to GitHub
* Payment PINs are never stored

---

## 🐛 Troubleshooting

* **"TemplateNotFound: payment.html"** → Ensure `payment.html` is in `templates/`
* **Invalid phone number** → Use `07XXXXXXXX` or `2547XXXXXXXX`
* **STK push fails** → Verify PayHero credentials and callback URL
* **No callback received** → Check ngrok or public URL accessibility

---

## 📁 Project Structure

```
mini_pesa/
├── app.py                 # Main Flask app
├── requirements.txt       # Python dependencies
├── templates/
│   └── payment.html       # Payment page
├── env.example            # Template environment variables
├── README.md              # Project instructions
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Open a Pull Request

---

**Built with ❤️ by DevMoses**

```

