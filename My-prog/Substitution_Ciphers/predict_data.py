import numpy as np
import joblib

# Load the model and label encoder
model = joblib.load('substitution_ciphers_rf_model.pkl')
label_encoder = joblib.load('substitution_ciphers_label_encoder.pkl')

# Define the mapping from numeric labels to algorithm names
label_to_algorithm = {
    0: 'Caesar Cipher',
    1: 'Vigenère Cipher',
    2: 'Affine Cipher',
    3: 'Playfair Cipher',
    4: 'Hill Cipher',
    # Add other mappings if necessary
}

# Preprocessing function (Ensure this matches the one used during training)
def preprocess_input(ciphertext, max_length=76):
    # Convert the text to a list of byte values (ASCII values for simplicity)
    encoded_input = list(ciphertext.encode())
    
    # Ensure the input is exactly 'max_length' features long
    if len(encoded_input) < max_length:
        # Pad the sequence if it's shorter than expected
        encoded_input.extend([0] * (max_length - len(encoded_input)))
    else:
        # Truncate the sequence if it's longer than expected
        encoded_input = encoded_input[:max_length]

    return np.array([encoded_input])  # Return as 2D array (1 sample)

# Input the ciphertext
ciphertext = input("Enter the ciphertext: ")

# Preprocess the input to match the model's expectations
input_data = preprocess_input(ciphertext)

# Make a prediction
predicted_label = model.predict(input_data)[0]

# Look up the algorithm name using the predicted label
algorithm_name = label_to_algorithm.get(predicted_label, "Unknown Algorithm")

# Output the predicted algorithm name
print(f"Predicted Algorithm: {algorithm_name}")
