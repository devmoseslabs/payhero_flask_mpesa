from flask import Flask, request, render_template, jsonify
import requests
import base64
import sqlite3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DATABASE'] = 'transactions.db'

# Environment variables
API_USERNAME = os.getenv('API_USERNAME')
API_PASSWORD = os.getenv('API_PASSWORD')
CALLBACK_URL = os.getenv('CALLBACK_URL')

# Database helper functions
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # Payments table only
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            amount REAL NOT NULL,
            reference TEXT NOT NULL UNIQUE,
            status TEXT DEFAULT 'pending',
            reason TEXT DEFAULT '',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def add_payment(phone, amount, reference, status='pending'):
    """Add a new payment record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO payments (phone, amount, reference, status) VALUES (?, ?, ?, ?)',
            (phone, amount, reference, status)
        )
        conn.commit()
        payment_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # If reference already exists, return its id
        cursor.execute('SELECT id FROM payments WHERE reference = ?', (reference,))
        row = cursor.fetchone()
        payment_id = row['id'] if row else None
    finally:
        conn.close()
    return payment_id

def update_payment_status(reference, new_status, reason=None):
    """Update payment status by reference and set reason and updated_at"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    print(f"Updating payment {reference} to {new_status}, reason: {reason}")
    
    cursor.execute(
        'UPDATE payments SET status = ?, reason = COALESCE(?, reason), updated_at = CURRENT_TIMESTAMP WHERE reference = ?',
        (new_status, reason, reference)
    )
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    print(f"Rows affected: {rows_affected}")
    return rows_affected > 0

def get_payment_by_reference(reference):
    """Get payment by reference"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE reference = ?', (reference,))
    payment = cursor.fetchone()
    conn.close()
    return payment

def log_callback(data):
    """Log callback data to JSON file"""
    try:
        if os.path.exists('callback_logs.json'):
            with open('callback_logs.json', 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'data': data,
            'received_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        logs.append(log_entry)
        
        # Keep only last 1000 entries
        if len(logs) > 1000:
            logs = logs[-1000:]
        
        with open('callback_logs.json', 'w') as f:
            json.dump(logs, f, indent=2)
            
        print(f"Callback logged successfully at {log_entry['received_at']}")
    except Exception as e:
        print(f"Error logging callback: {e}")

# Initialize database on startup
init_db()

# Routes
@app.route('/')
def index():
    """Main payment page"""
    return render_template('index.html')

@app.route('/pay', methods=['POST'])
def process_payment():
    """Process STK push payment with 254 prefix requirement"""
    try:
        # Get form data
        amount = request.form.get('amount')
        phone_number = request.form.get('phone_number')
        external_reference = request.form.get('external_reference')
        
        # Validate inputs
        if not all([amount, phone_number, external_reference]):
            return jsonify({'success': False, 'error': 'All fields are required!'}), 400
        
        try:
            amount = float(amount)
            if amount <= 0:
                return jsonify({'success': False, 'error': 'Amount must be positive!'}), 400
            if amount < 1:
                return jsonify({'success': False, 'error': 'Amount must be at least KES 1!'}), 400
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid amount format!'}), 400
        
        # Clean and validate phone number - Must be in 254XXXXXXXXX format
        phone_number = phone_number.replace(' ', '').replace('-', '').replace('+', '')
        
        # Ensure phone starts with 254 and is exactly 12 digits
        if not phone_number.startswith('254'):
            return jsonify({
                'success': False, 
                'error': 'Phone number must start with 254! Format: 2547XXXXXXXX or 2541XXXXXXXX'
            }), 400
        
        if len(phone_number) != 12:
            return jsonify({
                'success': False, 
                'error': 'Phone number must be 12 digits! Format: 2547XXXXXXXX (9 digits after 254)'
            }), 400
        
        # Validate that digits after 254 are numbers and start with valid Kenyan prefix
        digits_after_254 = phone_number[3:]
        if not digits_after_254.isdigit():
            return jsonify({
                'success': False, 
                'error': 'Phone number must contain only digits!'
            }), 400
        
        # Check if it starts with valid Kenyan mobile prefix (7 for Safaricom/Airtel, 1 for Telkom)
        if not digits_after_254.startswith(('7', '1')):
            return jsonify({
                'success': False, 
                'error': 'Invalid Kenyan mobile number! Must start with 2547 or 2541'
            }), 400
        
        # Validate reference length (8 characters)
        if len(external_reference) != 8:
            return jsonify({
                'success': False, 
                'error': 'Reference must be exactly 8 characters long!'
            }), 400
        
        # Prepare Basic Auth credentials
        credentials = f"{API_USERNAME}:{API_PASSWORD}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        # Prepare payment data
        payment_data = {
            'amount': int(amount),
            'phone_number': phone_number,
            'channel_id': os.getenv('PAYHERO_CHANNEL_ID'),
            'provider': 'm-pesa',
            'external_reference': external_reference,
            'callback_url': CALLBACK_URL
        }
        
        print(f"Sending payment request: {json.dumps(payment_data, indent=2)}")
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {encoded_credentials}',
            'User-Agent': 'PayFlow/1.0'
        }
        
        # Make API request to PayHero
        response = requests.post(
            'https://backend.payhero.co.ke/api/v2/payments',
            json=payment_data,
            headers=headers,
            timeout=30
        )
        
        print(f"PayHero response status: {response.status_code}")
        print(f"PayHero response: {response.text}")
        
        # Process response
        result = response.json()
        
        if response.status_code in (200, 201):
            if result.get('success') == True:
                # Add to database
                payment_id = add_payment(phone_number, amount, external_reference, 'initiated')
                
                return jsonify({
                    'success': True,
                    'message': 'M-Pesa STK initiated successfully! Check your phone.',
                    'reference': external_reference,
                    'payhero_reference': result.get('reference')
                })
            else:
                error_message = result.get('message', 'STK push failed to initiate')
                # Check for specific error messages
                if 'insufficient funds' in error_message.lower():
                    error_message = 'Insufficient funds in your M-Pesa account'
                elif 'timeout' in error_message.lower():
                    error_message = 'Payment timeout. Please try again'
                elif 'invalid phone' in error_message.lower():
                    error_message = 'Invalid phone number format'
                
                add_payment(phone_number, amount, external_reference, 'failed')
                
                return jsonify({'success': False, 'error': error_message}), 400
        else:
            error_message = result.get('message', f'HTTP Error {response.status_code}')
            add_payment(phone_number, amount, external_reference, 'failed')
            
            return jsonify({'success': False, 'error': error_message}), 400
            
    except requests.exceptions.RequestException as e:
        print(f"Network error: {str(e)}")
        return jsonify({'success': False, 'error': 'Network error occurred. Please check your connection and try again.'}), 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred. Please try again.'}), 500

@app.route("/callback", methods=["GET", "POST"])
def callback():
    """Handle PayHero callback"""
    print(f"=== CALLBACK REQUEST RECEIVED ===")
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json(force=True, silent=True)
            if data is None:
                raw_data = request.get_data(as_text=True)
                print(f"Raw data: {raw_data}")
                return jsonify({"error": "Invalid JSON"}), 400
        else:
            data = request.form.to_dict() or request.get_json(silent=True) or {}
            if not data:
                raw_data = request.get_data(as_text=True)
                try:
                    data = json.loads(raw_data) if raw_data else {}
                except:
                    data = {"raw": raw_data}
        
        print(f"Parsed data: {json.dumps(data, indent=2)}")
        
        # Extract data
        reference = None
        result_code = None
        mpesa_receipt = None
        result_desc = ""
        
        if "response" in data and isinstance(data["response"], dict):
            response_data = data["response"]
            reference = response_data.get("ExternalReference")
            result_code = response_data.get("ResultCode")
            mpesa_receipt = response_data.get("MpesaReceiptNumber")
            result_desc = response_data.get("ResultDesc", "")
        else:
            reference = data.get("external_reference") or data.get("ExternalReference") or data.get("reference")
            result_code = data.get("ResultCode") or data.get("result_code")
            mpesa_receipt = data.get("MpesaReceiptNumber") or data.get("mpesa_receipt")
            result_desc = data.get("ResultDesc") or data.get("result_desc") or data.get("message", "")
        
        print(f"Extracted - Reference: {reference}, ResultCode: {result_code}")
        
        # Map status
        mapped_status = 'pending'
        reason = result_desc
        
        if result_code == 0:
            mapped_status = 'completed'
            reason = f"Payment completed. M-Pesa Receipt: {mpesa_receipt}" if mpesa_receipt else "Payment completed successfully"
        elif result_code == 1:
            mapped_status = 'failed'
            if "insufficient" in result_desc.lower():
                reason = "Insufficient funds in M-Pesa account"
            else:
                reason = f"Payment failed: {result_desc}"
        elif result_code in [1031, 1032]:
            mapped_status = 'cancelled'
            reason = "Payment cancelled by user"
        elif result_code == 1037:
            mapped_status = 'timeout'
            reason = "Payment request timed out"
        elif result_code is not None:
            mapped_status = 'failed'
            reason = f"Payment failed (Error {result_code}): {result_desc}"
        
        print(f"Final mapping - Status: {mapped_status}, Reason: {reason}")
        
        # Update database if we have a reference
        if reference:
            print(f"Attempting to update payment: {reference} -> {mapped_status}")
            success = update_payment_status(reference, mapped_status, reason)
            
            if success:
                print(f"✅ SUCCESS: Updated {reference} to {mapped_status}")
            else:
                print(f"❌ FAILED: Could not update {reference}")
        else:
            print("⚠️  No reference found - cannot update database")
        
        # Log callback
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "reference": reference,
            "status": mapped_status,
            "result_code": result_code,
            "mpesa_receipt": mpesa_receipt,
            "reason": reason,
            "received_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "raw_data": data
        }
        log_callback(log_entry)
        
        return jsonify({
            "message": "Callback processed successfully",
            "reference": reference,
            "status": mapped_status
        }), 200
        
    except Exception as e:
        print(f"❌ CALLBACK ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        error_log = {
            "timestamp": datetime.now().isoformat(),
            "error": str(e),
            "traceback": traceback.format_exc(),
            "raw_data": request.get_data(as_text=True)
        }
        log_callback(error_log)
        
        return jsonify({"error": "Callback processing failed"}), 500

@app.route('/reconcile/<reference>')
def reconcile_payment(reference):
    """Re-check payment status"""
    # Check local DB
    payment = get_payment_by_reference(reference)
    
    if not payment:
        return jsonify({'error': 'Payment not found locally'}), 404
    
    local_status = payment['status']
    local_reason = payment['reason']
    
    # If payment is already completed or failed, return immediately
    if local_status in ['completed', 'failed', 'cancelled', 'timeout']:
        return jsonify({
            'reference': reference,
            'local_status': local_status,
            'local_reason': local_reason,
            'remote_status': local_status,
            'message': 'Payment status determined locally'
        }), 200
    
    # If API credentials missing, just return local status
    if not API_USERNAME or not API_PASSWORD:
        return jsonify({
            'reference': reference, 
            'local_status': local_status, 
            'remote_status': None, 
            'message': 'API credentials not configured'
        }), 200
    
    # Build Basic auth header
    credentials = f"{API_USERNAME}:{API_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'User-Agent': 'PayFlow/1.0'
    }
    
    url = f"https://backend.payhero.co.ke/api/v2/transaction-status?reference={reference}"
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        remote = resp.json() if resp.status_code == 200 else {}
        
        print(f"Reconcile response for {reference}: {remote}")
        
        # Try to extract remote status
        remote_status = None
        remote_reason = None
        if isinstance(remote, dict):
            data = remote.get('data') or remote
            if isinstance(data, dict):
                remote_status = data.get('status') or data.get('Status') or data.get('status_text')
                if isinstance(remote_status, str):
                    remote_status = remote_status.strip().lower()
                    if remote_status in ('success', 'successful', 'completed', 'paid'):
                        remote_status = 'completed'
                    elif remote_status in ('failed', 'failure', 'error'):
                        remote_status = 'failed'
                    elif remote_status in ('cancelled', 'canceled', 'cancel'):
                        remote_status = 'cancelled'
                    elif remote_status in ('timeout', 'timed_out', 'request_timeout'):
                        remote_status = 'timeout'
                    elif remote_status in ('queued', 'pending', 'initiated'):
                        remote_status = 'pending'
                
                remote_reason = data.get('message') or data.get('description') or data.get('ResultDesc') or None
        
        # If remote_status found and different, update local DB
        if remote_status and remote_status != local_status:
            update_payment_status(reference, remote_status, remote_reason)
            print(f"Updated payment {reference} from {local_status} to {remote_status}")
        
        return jsonify({
            'reference': reference,
            'local_status': local_status,
            'remote_status': remote_status,
            'remote_reason': remote_reason
        }), 200
        
    except requests.exceptions.RequestException as e:
        print(f"Reconcile request error: {e}")
        return jsonify({
            'error': 'Network error during reconcile', 
            'detail': str(e),
            'local_status': local_status
        }), 502
    except Exception as ex:
        print(f"Unexpected reconcile error: {ex}")
        return jsonify({
            'error': 'Unexpected error', 
            'detail': str(ex),
            'local_status': local_status
        }), 500

if __name__ == '__main__':
    print("Starting Flask application...")
    print("Database initialized with payments table")
    print(f"Callback URL: {CALLBACK_URL}")
    app.run(debug=True, port=7000, host='0.0.0.0')
