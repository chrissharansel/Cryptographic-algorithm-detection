import numpy as np
import joblib

# Load the trained model and label encoder
model = joblib.load('hash_functions_rf_model.pkl')
label_encoder = joblib.load('hash_functions_label_encoder.pkl')

# Function to preprocess input data
def preprocess_input(ciphertext_hex, max_len):
    print(f"Original input: '{ciphertext_hex}'")  # Debug print
    
    # Clean the input data
    ciphertext_hex = ciphertext_hex.strip().replace(' ', '')  # Remove spaces
    
    # Check if the input is valid hex
    if not all(c in '0123456789abcdefABCDEF' for c in ciphertext_hex):
        raise ValueError("Invalid hexadecimal input")
    
    # Convert hex to bytes and then to list of integers
    try:
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        raise ValueError("Error converting hex to bytes. Ensure input is valid hex.")
    
    feature_vector = list(ciphertext_bytes)
    
    # Pad or truncate the feature vector to match the trained model's input size
    if len(feature_vector) < max_len:
        feature_vector.extend([0] * (max_len - len(feature_vector)))
    elif len(feature_vector) > max_len:
        feature_vector = feature_vector[:max_len]
    
    return np.array(feature_vector).reshape(1, -1)

# Maximum length used during training (adjust as needed)
max_len = 32  # Ensure this matches the length used in training

# Input ciphertext (hex format)
ciphertext_hex = input("Enter the ciphertext (in hex format): ")

try:
    # Preprocess the input data
    input_data = preprocess_input(ciphertext_hex, max_len)

    # Predict the algorithm
    predicted_label_encoded = model.predict(input_data)
    predicted_label = label_encoder.inverse_transform(predicted_label_encoded)

    print(f"The predicted algorithm is: {predicted_label[0]}")
except ValueError as e:
    print(f"Error: {e}")
