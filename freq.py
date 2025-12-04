from collections import Counter

cipher_text = "slaz tlla avupnoa ha aol whyr"
english_order = list("etaoinshrdlcumwfgypbvkjxqz")

def get_letter_frequency(text):
    text = text.replace(" ", "").lower()
    freq = Counter(text)
    return [letter for letter, _ in freq.most_common()]

def make_substitution_key(sorted_letters, freq_order):
    return {c: e for c, e in zip(sorted_letters, freq_order)}

actual_key = {
    's': 'l', 'l': 'e', 'a': 't', 'z': 's', 't': 'm', 'v': 'o',
    'u': 'n', 'p': 'i', 'n': 'g', 'o': 'h', 'h': 'a', 'w': 'p', 'y': 'r', 'r': 'k'
}

def decode_text(text, key):
    result = ""
    for char in text:
        if char == ' ':
            result += ' '
        else:
            result += key.get(char, '_')
    return result

def compare_keys(guess_key, correct_key):
    diff = {}
    for letter in correct_key:
        guess = guess_key.get(letter, '_')
        correct = correct_key[letter]
        if guess != correct:
            diff[letter] = (guess, correct)
    return diff

# Main execution
sorted_letters = get_letter_frequency(cipher_text)
guess_key = make_substitution_key(sorted_letters, english_order)
diff = compare_keys(guess_key, actual_key)
decoded_guess = decode_text(cipher_text, guess_key)
decoded_actual = decode_text(cipher_text, actual_key)

print("Cipher Letter Frequency (most to least):")
print(" ".join(sorted_letters))

print("\nStandard English Letter Frequency Order:")
print(" ".join(english_order[:len(sorted_letters)]))

print("\nInitial Substitution Key (frequency-based guess):")
for c in sorted_letters:
    print(f"{c} → {guess_key[c]}")

print("\nDecoded Text Using Frequency-Based Guess:")
print(decoded_guess)

print("\nCorrect Substitution Key:")
for c in sorted(actual_key.keys()):
    print(f"{c} → {actual_key[c]}")



print("\nDecoded Text Using Correct Key:")
print(decoded_actual)
