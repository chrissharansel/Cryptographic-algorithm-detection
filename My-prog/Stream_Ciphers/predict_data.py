import joblib
import numpy as np

# Load the trained model
model = joblib.load('stream_ciphers_rf_model.pkl')

# Load the label encoder
label_encoder = joblib.load('stream_ciphers_label_encoder.pkl')

# Determine fixed size for padding/truncation
FIXED_SIZE = 64

# Function to preprocess the input data (ciphertext)
def preprocess_input(data, max_length=64):
    # Convert hex string back to bytes
    data_bytes = bytes.fromhex(data)
    # Convert bytes to numeric array
    data_numeric = list(data_bytes)
    data_padded = data_numeric[:max_length] + [0] * (max_length - len(data_numeric))
    return np.array(data_padded).reshape(1, -1)

# Example user input for ciphertext
ciphertext = input("Enter the ciphertext (in hex format): ")

# Preprocess the ciphertext
input_data = preprocess_input(ciphertext, FIXED_SIZE)

# Predict the algorithm
predicted_label = model.predict(input_data)
predicted_algorithm = label_encoder.inverse_transform(predicted_label)

print(f'The predicted algorithm is: {predicted_algorithm[0]}')
