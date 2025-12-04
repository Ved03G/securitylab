import math


def egcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("No modular inverse (e, φ(n) not coprime)")
    return x % m


def text_to_int_base26(text: str) -> int:
    value = 0
    for ch in text:
        if 'a' <= ch <= 'z':
            value = value * 26 + (ord(ch) - ord('a'))
        else:
            raise ValueError("Only lowercase letters allowed for base-26 mode")
    return value


def int_to_text_base26(n: int) -> str:
    if n == 0:
        return "a"
    chars = []
    while n > 0:
        n, r = divmod(n, 26)
        chars.append(chr(r + ord('a')))
    return ''.join(reversed(chars))


def utf8_to_bytes(text: str) -> bytes:
    return text.encode("utf-8")


def bytes_to_utf8(b: bytes) -> str:
    return b.decode("utf-8", errors="ignore")


print("=== RSA Demo ===")
p = int(input("Enter prime p: "))
q = int(input("Enter prime q: "))
e = int(input("Enter public exponent e: "))

n = p * q
phi = (p - 1) * (q - 1)
d_gcd = math.gcd(e, phi)
while d_gcd != 1:
    print(f"Public exponent e must be coprime with φ(n)={phi}. Current gcd(e, φ(n)) = {d_gcd}.")
    e = int(input("Enter a different public exponent e: "))
    d_gcd = math.gcd(e, phi)
d = modinv(e, phi)
print(f"\np={p}, q={q}, e={e}, n={n}, φ(n)={phi}, d={d}")

plaintext = input("\nEnter plaintext: ")
if plaintext.isdigit():
    m = int(plaintext)
    decode_mode = "int"
elif plaintext.isalpha() and plaintext.islower():
    m = text_to_int_base26(plaintext)
    decode_mode = "base26"
else:
    data_bytes = utf8_to_bytes(plaintext)
    m = int.from_bytes(data_bytes, "big")
    decode_mode = "utf8"

if m >= n:
    print(f"\nEncoded message integer m={m} must be smaller than n={n}.")
    print("Please choose larger primes (p, q) or shorter plaintext.")
    # Reprompt for p, q, e until n > m and gcd(e, φ(n)) == 1
    while True:
        p = int(input("Enter prime p: "))
        q = int(input("Enter prime q: "))
        e = int(input("Enter public exponent e: "))
        n = p * q
        phi = (p - 1) * (q - 1)
        if m >= n:
            print(f"n={n} still ≤ m={m}. Pick larger primes.")
            continue
        d_gcd = math.gcd(e, phi)
        if d_gcd != 1:
            print(f"gcd(e, φ(n))={d_gcd} ≠ 1. Pick a different e.")
            continue
        d = modinv(e, phi)
        print(f"\np={p}, q={q}, e={e}, n={n}, φ(n)={phi}, d={d}")
        break

print(f"\nPlaintext = {plaintext}")
print(f"Encoded integer m = {m}")

c = pow(m, e, n)
print(f"\nCiphertext = {c}")

m_rec = pow(c, d, n)
if decode_mode == "int":
    decrypted = str(m_rec)
elif decode_mode == "base26":
    decrypted = int_to_text_base26(m_rec)
else:
    b = m_rec.to_bytes((m_rec.bit_length() + 7) // 8, "big")
    decrypted = bytes_to_utf8(b)

print(f"Decrypted plaintext = {decrypted}")
