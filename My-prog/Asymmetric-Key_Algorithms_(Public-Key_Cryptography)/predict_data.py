import joblib
import numpy as np

# Load the trained model
model = joblib.load('asymmetric_key_algorithms_rf_model.pkl')

# Load the label encoder
label_encoder = joblib.load('asymmetric_key_algorithms_label_encoder.pkl')

# Function to preprocess the input data (ciphertext)
def preprocess_input(data, max_length=256):
    data_bytes = bytes.fromhex(data)
    data_numeric = list(data_bytes)
    data_padded = data_numeric[:max_length] + [0] * (max_length - len(data_numeric))
    return np.array(data_padded).reshape(1, -1)

# Example user input for ciphertext
ciphertext = input("Enter the ciphertext (in hex format): ")

# Preprocess the ciphertext
input_data = preprocess_input(ciphertext)

# Predict the algorithm
predicted_label = model.predict(input_data)
predicted_algorithm = label_encoder.inverse_transform(predicted_label)

print(f'The predicted algorithm is: {predicted_algorithm[0]}')
