document.addEventListener('DOMContentLoaded', function() {
    // Update work factor display
    const workFactor = document.getElementById('workFactor');
    const workFactorValue = document.getElementById('workFactorValue');
    const workFactorGroup = document.getElementById('workFactorGroup');
    const hashAlgorithm = document.getElementById('hashAlgorithm');

    // Show/hide work factor based on algorithm
    function updateWorkFactorVisibility() {
        workFactorGroup.style.display = 
            ['bcrypt', 'argon2'].includes(hashAlgorithm.value) ? 'block' : 'none';
    }

    hashAlgorithm.addEventListener('change', updateWorkFactorVisibility);
    updateWorkFactorVisibility();

    workFactor.addEventListener('input', function() {
        workFactorValue.textContent = this.value;
    });

    // Handle password hashing
    document.getElementById('hashForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const password = document.getElementById('password').value;
        const algorithm = hashAlgorithm.value;
        
        try {
            const response = await fetch('/hash', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    password: password,
                    algorithm: algorithm,
                    workFactor: parseInt(workFactor.value)
                }),
            });
            
            const data = await response.json();
            
            document.getElementById('saltValue').textContent = data.salt;
            document.getElementById('concatenationOrder').textContent = data.concatenation;
            document.getElementById('hashValue').textContent = data.hash;
            document.getElementById('hashTiming').textContent = `${data.timing_ms} ms`;
            
            document.getElementById('hashResults').style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while hashing the password.');
        }
    });

    // Handle encryption
    document.getElementById('encryptForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const plaintext = document.getElementById('plaintext').value;
        
        try {
            const response = await fetch('/encrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: plaintext
                }),
            });
            
            const data = await response.json();
            
            document.getElementById('encryptedValue').textContent = data.encrypted_base64;
            document.getElementById('encryptTiming').textContent = `${data.encryption_timing_ms} ms`;
            
            document.getElementById('encryptResults').style.display = 'block';
            document.getElementById('decryptResults').style.display = 'none';
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while encrypting the data.');
        }
    });

    // Handle decryption
    document.getElementById('decryptButton').addEventListener('click', async function() {
        const encryptedData = document.getElementById('encryptedValue').textContent;
        
        try {
            const response = await fetch('/decrypt', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: encryptedData
                }),
            });
            
            const data = await response.json();
            
            document.getElementById('decryptedValue').textContent = data.decrypted;
            document.getElementById('decryptTiming').textContent = `${data.decryption_timing_ms} ms`;
            
            document.getElementById('decryptResults').style.display = 'block';
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while decrypting the data.');
        }
    });
});
