import numpy as np

# gdc 
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Calculate the modular inverse of a matrix
def find_mod_inverse(a, m):
    # Finds the number x such that (a * x) % m == 1
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Find the key 
def generate_hill_key(n, m=26):
    while True:
        # 1. Create a random n x n matrix
        key = np.random.randint(0, m, (n, n))
        
        # 2. Calculate determinant
        det = int(np.round(np.linalg.det(key))) % m
        
        # 3. Check if determinant is coprime to m
        if det != 0 and gcd(det, m) == 1:
            return key

# Encryption 
def encryption(message, key):
    # Conversion letters to numbers
    message_num = [ord(char) - ord('A') for char in message]
    
    # Padding
    while len(message_num) % key.shape[0] != 0:
        message_num.append(25)  # Padding with 'Z' (25)
    
    # Reshape the message into blocks
    message_blocks = np.array(message_num).reshape(-1, key.shape[0])
    
    # Encrypt each block
    encrypted_blocks = (message_blocks @ key) % 26
    
    # Convert back to characters
    encrypted_message = ''.join(chr(num + ord('A')) for num in encrypted_blocks.flatten())
    
    return encrypted_message, encrypted_blocks

# Decryption 
def decryption(encrypted_message, key):
    n = key.shape[0]
    # 1. Get the Determinant (Properly rounded!)
    det = int(np.round(np.linalg.det(key)))
    det_mod = det % 26
    det_inv = find_mod_inverse(det_mod, 26)

    if det_inv is None:
        raise ValueError("Key not invertible mod 26")

    # 2. Find the Adjugate Matrix using the floating point inverse
    # Adjugate = det * inv(matrix)
    # We use round() then int() to stop 1.0 becoming 0
    adjugate = np.round(np.linalg.inv(key) * det).astype(int) % 26

    # 3. Multiply by the modular inverse of the determinant
    inverse_key_mod = (det_inv * adjugate) % 26

    # 4. Decrypt (Message @ Inverse_Key)
    encrypted_num = [ord(char) - ord('A') for char in encrypted_message]
    encrypted_blocks = np.array(encrypted_num).reshape(-1, n)
    
    decrypted_blocks = (encrypted_blocks @ inverse_key_mod) % 26
    
    # 5. Build final string
    decrypted_message = ''.join(chr(int(np.round(num)) + ord('A')) for num in decrypted_blocks.flatten())
    
    return decrypted_message

# Padding removal (if needed)
def remove_padding(message):
    return message.rstrip('Z')

# Main loop
while True:
    print("Hill Cipher")
    print("Enter message:")
    message = input().upper().replace(" ", "")  # Remove spaces and convert to uppercase
    if not message: 
        print("Message cannot be empty. Please try again.")
        continue
    print("Enter key size (n x n):")
    try:        
        n = int(input())
        if n <= 0:            
            print("Key size must be a positive integer. Please try again.")
            continue
    except ValueError:
        print("Invalid input for key size. Please enter a positive integer.")
        continue

    key = generate_hill_key(n)
    print("Generated Key:")
    print(key)

    print("Encrypting message "+ message )

    encrypted_message, encrypted_blocks= encryption(message, key)
    print("Encrypted Message:")
    print(encrypted_message + "\nAs matrix: \n" + str(encrypted_blocks))

    decrypted_message = decryption(encrypted_message, key)
    print("Decrypted Message:")
    print(decrypted_message)

    if(decrypted_message[len(decrypted_message) - 1] == 'Z'):
        print("With possible padding removed:")
        print(remove_padding(decrypted_message))    
