import numpy as np

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def find_mod_inverse(a, m):
    """Finds the multiplicative inverse of a modulo m."""
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def get_matrix_determinant(matrix):
    """Calculates determinant using pure integers to avoid float betrayal."""
    return int(np.round(np.linalg.det(matrix)))

def get_integer_adjugate(matrix):
    """Calculates the adjugate matrix using integer math for 2x2 or 3x3."""
    n = len(matrix)
    adjugate = np.zeros((n, n), dtype=int)
    
    if n == 2:
        adjugate[0, 0] = matrix[1, 1]
        adjugate[0, 1] = -matrix[0, 1]
        adjugate[1, 0] = -matrix[1, 0]
        adjugate[1, 1] = matrix[0, 0]
    else:
        # For 3x3 and up, we use the cofactor method
        for i in range(n):
            for j in range(n):
                # Create the minor matrix
                minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                # Calculate cofactor: (-1)^(i+j) * det(minor)
                cofactor = ((-1)**(i + j)) * get_matrix_determinant(minor)
                # Adjugate is the transpose of the cofactor matrix
                adjugate[j, i] = cofactor
    return adjugate

def get_hill_inverse(key, m=26):
    det = get_matrix_determinant(key)
    det_mod = det % m
    det_inv = find_mod_inverse(det_mod, m)
    
    if det_inv is None:
        return None
    
    adjugate = get_integer_adjugate(key)
    # Final step: (det_inv * adjugate) mod m
    return (det_inv * adjugate) % m

def encryption(text, key):
    n = key.shape[0]
    text = text.upper().replace(" ", "")
    while len(text) % n != 0:
        text += 'Z'
    nums = [ord(c) - ord('A') for c in text]
    
    # We reshape and TRANSPOSE to make each block a column
    blocks = np.array(nums).reshape(-1, n).T
    
    # NEW MATH: Key @ Blocks
    cipher_nums = (key @ blocks) % 26
    
    # Transpose back to read it correctly
    return "".join(chr(int(val) + ord('A')) for val in cipher_nums.T.flatten())

def decryption(cipher, key):
    n = key.shape[0]
    inv_key = get_hill_inverse(key)
    if inv_key is None: return "ERROR: Key not invertible!"
    
    nums = [ord(c) - ord('A') for c in cipher]
    blocks = np.array(nums).reshape(-1, n).T
    
    # NEW MATH: Inv_Key @ Blocks
    plain_nums = (inv_key @ blocks) % 26
    
    # Transpose back to read it correctly
    return "".join(chr(int(np.round(val)) + ord('A')) for val in plain_nums.T.flatten())

def main():
    print("--- HILL CIPHER SYSTEM ---")
    size = int(input("Enter matrix size (e.g., 2 or 3): "))
    
    # Generate a valid key
    valid_found = False
    while not valid_found:
        key = np.random.randint(0, 26, (size, size))
        if find_mod_inverse(get_matrix_determinant(key) % 26, 26) is not None:
            valid_found = True
    
    print("\nGenerated Valid Key Matrix:")
    print(key)
    
    while True:
        user_msg = input("\nEnter message to encrypt (or 'exit'): ")
        if user_msg.lower() == 'exit': break
        
        enc = encryption(user_msg, key)
        dec = decryption(enc, key)
        
        print(f"Encrypted: {enc}")
        print(f"Decrypted: {dec}")

if __name__ == "__main__":
    main()
