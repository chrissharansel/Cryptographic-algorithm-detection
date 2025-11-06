import joblib
import numpy as np
from Crypto.Cipher import AES, DES, Blowfish, DES3
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Load the trained model
model = joblib.load('block_ciphers_rf_model.pkl')

# Load the label encoder
label_encoder = joblib.load('block_ciphers_label_encoder.pkl')

# Function to preprocess the input data (ciphertext)
def preprocess_input(data, max_length=256):
    data_bytes = bytes.fromhex(data)
    data_numeric = list(data_bytes)
    data_padded = data_numeric[:max_length] + [0] * (max_length - len(data_numeric))
    return np.array(data_padded).reshape(1, -1)

# Symmetric encryption examples
def encrypt_with_aes(plaintext):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return ciphertext.hex()

def encrypt_with_des(plaintext):
    key = get_random_bytes(8)
    cipher = DES.new(key, DES.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext.encode(), DES.block_size))
    return ciphertext.hex()

def encrypt_with_blowfish(plaintext):
    key = get_random_bytes(16)
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext.encode(), Blowfish.block_size))
    return ciphertext.hex()

def encrypt_with_3des(plaintext):
    key = get_random_bytes(24)
    cipher = DES3.new(key, DES3.MODE_CBC)
    ciphertext = cipher.iv + cipher.encrypt(pad(plaintext.encode(), DES3.block_size))
    return ciphertext.hex()

# Ask user for plaintext input
plaintext = input("Enter the plaintext: ")

# Ask user to choose the encryption algorithm
print("Choose the encryption algorithm:")
print("1. AES")
print("2. DES")
print("3. Blowfish")
print("4. 3DES")
choice = int(input("Enter your choice (1/2/3/4): "))

# Encrypt the plaintext based on user choice
if choice == 1:
    ciphertext = encrypt_with_aes(plaintext)
elif choice == 2:
    ciphertext = encrypt_with_des(plaintext)
elif choice == 3:
    ciphertext = encrypt_with_blowfish(plaintext)
elif choice == 4:
    ciphertext = encrypt_with_3des(plaintext)
else:
    raise ValueError("Invalid choice")

# Preprocess the ciphertext
input_data = preprocess_input(ciphertext)

# Predict the algorithm
predicted_label = model.predict(input_data)
predicted_algorithm = label_encoder.inverse_transform(predicted_label)

print(f'The predicted algorithm is: {predicted_algorithm[0]}')
