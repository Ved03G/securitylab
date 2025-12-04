import math

# ==========================================
# 1, 2, 3. Caesar / Additive / Shift Cipher
# ==========================================
def encrypt_shift(text, key):
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            # Formula: (P + K) % 26
            result += chr((ord(char) - base + key) % 26 + base)
        else:
            result += char
    return result

# ==========================================
# 4. Multiplicative Cipher
# ==========================================
def encrypt_multiplicative(text, key):
    # Key must be coprime to 26 (gcd(key, 26) == 1)
    if math.gcd(key, 26) != 1:
        return "Error: Key must be coprime to 26 (e.g., 3, 5, 7, 11...)"
    
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            # Formula: (P * K) % 26
            result += chr(((ord(char) - base) * key) % 26 + base)
        else:
            result += char
    return result

# ==========================================
# 5. Affine Cipher
# ==========================================
def encrypt_affine(text, a, b):
    # Formula: (ax + b) % 26
    if math.gcd(a, 26) != 1:
        return "Error: Key 'a' must be coprime to 26."
        
    result = ""
    for char in text:
        if char.isalpha():
            base = 65 if char.isupper() else 97
            p = ord(char) - base
            c = (a * p + b) % 26
            result += chr(c + base)
        else:
            result += char
    return result

# ==========================================
# 6. Autokey Cipher
# ==========================================
def encrypt_autokey(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    
    # Generate the running key: Keyword + Plaintext
    full_key = key + text
    full_key = full_key[:len(text)] # Trim to match text length
    
    result = ""
    for i in range(len(text)):
        p = ord(text[i]) - 65
        k = ord(full_key[i]) - 65
        c = (p + k) % 26
        result += chr(c + 65)
    return result

# ==========================================
# 7. Vigenère Cipher
# ==========================================
def encrypt_vigenere(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    result = ""
    
    for i in range(len(text)):
        p = ord(text[i]) - 65
        k = ord(key[i % len(key)]) - 65 # Cycle through key
        c = (p + k) % 26
        result += chr(c + 65)
    return result

# ==========================================
# 8. Rail Fence Cipher
# ==========================================
def encrypt_railfence(text, depth):
    text = text.replace(" ", "")
    # Create a matrix of placeholder dots
    rail = [['\n' for i in range(len(text))] for j in range(depth)]
    
    dir_down = False
    row, col = 0, 0
    
    for char in text:
        if row == 0 or row == depth - 1:
            dir_down = not dir_down
            
        rail[row][col] = char
        col += 1
        
        if dir_down:
            row += 1
        else:
            row -= 1
            
    # Read matrix row by row
    result = []
    for i in range(depth):
        for j in range(len(text)):
            if rail[i][j] != '\n':
                result.append(rail[i][j])
    return "".join(result)

# ==========================================
# 9. Keyed Transposition (Columnar)
# ==========================================
def encrypt_keyed_transposition(text, key):
    text = text.replace(" ", "")
    
    # Pad text to fit columns perfectly
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    pad_len = (num_rows * num_cols) - len(text)
    text += 'X' * pad_len
    
    # Get order of columns based on key (e.g., "HACK" -> 2, 0, 1, 3)
    # Create tuple (char, index) and sort by char
    key_order = sorted([(k, i) for i, k in enumerate(key)])
    
    # Write into grid
    grid = []
    for i in range(num_rows):
        grid.append(text[i*num_cols : (i+1)*num_cols])
        
    # Read columns based on sorted key order
    result = ""
    for k_char, col_index in key_order:
        for row in range(num_rows):
            result += grid[row][col_index]
            
    return result

# ==========================================
# 10. Hill Cipher (2x2 Matrix)
# ==========================================
def encrypt_hill(text, key_matrix):
    text = text.upper().replace(" ", "")
    # Pad if odd length
    if len(text) % 2 != 0:
        text += 'X'
        
    result = ""
    for i in range(0, len(text), 2):
        # Take pairs of letters
        pair = [ord(text[i]) - 65, ord(text[i+1]) - 65]
        
        # Matrix multiplication: [C1, C2] = [P1, P2] * KeyMatrix
        c1 = (pair[0] * key_matrix[0][0] + pair[1] * key_matrix[1][0]) % 26
        c2 = (pair[0] * key_matrix[0][1] + pair[1] * key_matrix[1][1]) % 26
        
        result += chr(c1 + 65) + chr(c2 + 65)
    return result

# ==========================================
# 11. Playfair Cipher
# ==========================================
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    seen = set()
    
    # Add key characters first
    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)
            
    # Add remaining alphabet
    for char in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in seen:
            matrix.append(char)
            
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_pos(matrix, char):
    for r, row in enumerate(matrix):
        if char in row:
            return r, row.index(char)
    return None

def encrypt_playfair(text, key):
    matrix = generate_playfair_matrix(key)
    text = text.upper().replace("J", "I").replace(" ", "")
    
    # Prepare Digraphs (handle repeats like HELLO -> HELXLO)
    prepared_text = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        
        if a == b:
            prepared_text += a + 'X'
            i += 1
        else:
            prepared_text += a + b
            i += 2
            
    if len(prepared_text) % 2 != 0:
        prepared_text += 'X'
        
    result = ""
    for i in range(0, len(prepared_text), 2):
        r1, c1 = find_pos(matrix, prepared_text[i])
        r2, c2 = find_pos(matrix, prepared_text[i+1])
        
        if r1 == r2: # Same Row
            result += matrix[r1][(c1+1)%5] + matrix[r2][(c2+1)%5]
        elif c1 == c2: # Same Col
            result += matrix[(r1+1)%5][c1] + matrix[(r2+1)%5][c2]
        else: # Rectangle
            result += matrix[r1][c2] + matrix[r2][c1]
            
    return result


# ==========================================
# MAIN MENU
# ==========================================
if __name__ == "__main__":
    while True:
        print("\n--- SECURITY LAB PRACTICALS ---")
        print("1. Caesar Cipher")
        print("2. Additive Cipher")
        print("3. Shift Cipher")
        print("4. Multiplicative Cipher")
        print("5. Affine Cipher")
        print("6. Autokey Cipher")
        print("7. Vigenère Cipher")
        print("8. Rail Fence Cipher")
        print("9. Keyed Transposition Cipher")
        print("10. Hill Cipher")
        print("11. Playfair Cipher")
        print("0. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '0': break
        
        msg = input("Enter message: ")
        
        if choice in ['1', '2', '3']:
            k = int(input("Enter Shift Key (int): "))
            print("Encrypted:", encrypt_shift(msg, k))
            
        elif choice == '4':
            k = int(input("Enter Multiplier Key (coprime to 26): "))
            print("Encrypted:", encrypt_multiplicative(msg, k))
            
        elif choice == '5':
            a = int(input("Enter Key A (Multiplicative part): "))
            b = int(input("Enter Key B (Additive part): "))
            print("Encrypted:", encrypt_affine(msg, a, b))
            
        elif choice == '6':
            k = input("Enter Keyword: ")
            print("Encrypted:", encrypt_autokey(msg, k))
            
        elif choice == '7':
            k = input("Enter Keyword: ")
            print("Encrypted:", encrypt_vigenere(msg, k))
            
        elif choice == '8':
            d = int(input("Enter Depth (Rails): "))
            print("Encrypted:", encrypt_railfence(msg, d))
            
        elif choice == '9':
            k = input("Enter Keyword (e.g., HACK): ")
            print("Encrypted:", encrypt_keyed_transposition(msg, k))
            
        elif choice == '10':
            print("Using fixed 2x2 Key Matrix [[3, 3], [2, 5]]")
            # This matrix is invertible modulo 26
            key_matrix = [[3, 3], [2, 5]] 
            print("Encrypted:", encrypt_hill(msg, key_matrix))
            
        elif choice == '11':
            k = input("Enter Keyword: ")
            print("Encrypted:", encrypt_playfair(msg, k))
