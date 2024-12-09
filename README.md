# Cryptographic Concepts Demo

This Flask application demonstrates various cryptographic concepts including password hashing, encryption/decryption, and encoding/decoding workflows. It provides an interactive interface to understand how these processes work.

## Features

- Password hashing with multiple algorithms (SHA-256, SHA-3, BCrypt, Argon2)
- Demonstration of salt and pepper usage in password hashing
- Data encryption and decryption using Fernet
- Base64 encoding/decoding demonstration
- Interactive UI showing each step of the process
- Performance timing for different algorithms
- Adjustable work factors for password hashing

## Setup Instructions

- Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# .\venv\Scripts\activate
```

- Install dependencies:

```bash
pip install -r requirements.txt
```

- Run the Flask application:

```bash
python app.py
```

- Open your web browser and navigate to: http://127.0.0.1:5000

## Usage

### Password Hashing

1. Enter a sample password
2. Choose a hashing algorithm from the dropdown
3. Adjust the work factor (for BCrypt and Argon2)
4. Submit to see the complete hashing process

### Encryption/Decryption

1. Enter text to encrypt
2. View the encrypted and Base64 encoded result
3. Click "Decrypt" to verify the original data

## Security Note

This is a demonstration application intended for educational purposes. The pepper value and encryption keys are hardcoded in the application for demonstration. In a production environment, these values should be stored securely and never exposed in the source code.

## Requirements

- Python 3.7+
- Flask
- cryptography
- bcrypt
- argon2-cffi

## Project Structure

```plain
crypt-concepts-flask-demo/
├── README.md
├── requirements.txt
├── app.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── templates/
    └── index.html
```
