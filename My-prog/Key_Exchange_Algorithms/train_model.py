import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Function to load dataset with error handling for encoding
def load_dataset(file_name):
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_name, encoding=encoding)
            print(f"Successfully loaded dataset with encoding: {encoding}")
            return df
        except UnicodeDecodeError:
            print(f"Failed to load dataset with encoding: {encoding}")
    raise ValueError("Failed to load dataset with available encodings.")

# Function to convert hex to bytes with error handling
def safe_hex_to_bytes(hex_str):
    try:
        return list(bytes.fromhex(hex_str))
    except ValueError:
        print(f"Invalid hex data: {hex_str}")
        return []

# Load dataset
df = load_dataset('key_exchange_algorithms_dataset.csv')

# Preprocess data
print("Preprocessing data...")
df['ciphertext'] = df['ciphertext'].apply(safe_hex_to_bytes)
df = df[df['ciphertext'].apply(lambda x: len(x) > 0)]  # Filter out rows with invalid data

# Find the maximum length of ciphertexts for padding
max_length = max(df['ciphertext'].apply(len))

# Pad or truncate ciphertexts to a consistent length
def pad_or_truncate(ciphertext, length):
    return ciphertext + [0] * (length - len(ciphertext)) if len(ciphertext) < length else ciphertext[:length]

df['ciphertext'] = df['ciphertext'].apply(lambda x: pad_or_truncate(x, max_length))

X = np.array(df['ciphertext'].tolist())
y = df['algorithm']

# Encode labels
print("Encoding labels...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
print("Training model...")
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model and label encoder
print("Saving model and label encoder...")
joblib.dump(model, 'key_exchange_algorithms_rf_model.pkl')
joblib.dump(label_encoder, 'key_exchange_algorithms_label_encoder.pkl')

print("Model training and saving completed.")
