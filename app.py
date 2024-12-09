from flask import Flask, render_template, request, jsonify
import os
import time
import hashlib
import bcrypt
import argon2
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

app = Flask(__name__)

# This would normally be an environment variable
PEPPER = b"your_secure_pepper_value"
# Generate a key for Fernet encryption
ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

def time_function(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, (end_time - start_time) * 1000  # Convert to milliseconds

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hash', methods=['POST'])
def hash_password():
    data = request.get_json()
    password = data['password'].encode()
    algorithm = data['algorithm']
    work_factor = int(data.get('workFactor', 12))
    
    # Generate a unique salt
    salt = os.urandom(16)
    
    results = {
        'salt': base64.b64encode(salt).decode(),
        'pepper_used': True,
        'concatenation': 'password + salt + pepper'
    }
    
    if algorithm == 'sha256':
        combined = password + salt + PEPPER
        hash_obj, timing = time_function(
            lambda: hashlib.sha256(combined).hexdigest()
        )
        results['hash'] = hash_obj
        
    elif algorithm == 'sha3':
        combined = password + salt + PEPPER
        hash_obj, timing = time_function(
            lambda: hashlib.sha3_256(combined).hexdigest()
        )
        results['hash'] = hash_obj
        
    elif algorithm == 'bcrypt':
        # BCrypt automatically handles the salt, but we'll show it for demonstration
        hash_obj, timing = time_function(
            lambda: bcrypt.hashpw(password + PEPPER, bcrypt.gensalt(work_factor))
        )
        results['hash'] = hash_obj.decode()
        
    elif algorithm == 'argon2':
        # Argon2 configuration for demonstration
        hash_obj, timing = time_function(
            lambda: argon2.hash_password(
                password + PEPPER,
                salt,
                time_cost=work_factor,
                memory_cost=65536,
                parallelism=4
            )
        )
        results['hash'] = hash_obj.decode()
    
    results['timing_ms'] = round(timing, 2)
    return jsonify(results)

@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    data = request.get_json()
    # Encode a string to bytes
    plaintext = data['data'].encode()
    
    # Encrypt
    encrypted_data, encrypt_timing = time_function(
        lambda: fernet.encrypt(plaintext)
    )
    
    # Encode in base64, then decode to a string that represents bytes
    encoded_data = base64.b64encode(encrypted_data).decode()
    
    return jsonify({
        'encrypted_base64': encoded_data,
        'encryption_timing_ms': round(encrypt_timing, 2)
    })

@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    data = request.get_json()
    # Convert base64 to bytes
    encoded_data = data['data'].encode()
    
    # Decode base64
    encrypted_data = base64.b64decode(encoded_data)
    
    # Decrypt
    decrypted_data, decrypt_timing = time_function(
        lambda: fernet.decrypt(encrypted_data)
    )
    
    return jsonify({
        'decrypted': decrypted_data.decode(),
        'decryption_timing_ms': round(decrypt_timing, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)
