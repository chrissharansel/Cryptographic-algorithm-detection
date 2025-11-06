import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the dataset with a specified encoding
try:
    df = pd.read_csv('stream_ciphers_dataset.csv', encoding='utf-8')
except UnicodeDecodeError:
    # Try a different encoding if utf-8 fails
    df = pd.read_csv('stream_ciphers_dataset.csv', encoding='latin1')

# Encode the algorithm labels
label_encoder = LabelEncoder()
df['algorithm'] = label_encoder.fit_transform(df['algorithm'])

# Save the label encoder
joblib.dump(label_encoder, 'stream_ciphers_label_encoder.pkl')

# Determine fixed size for padding/truncation
FIXED_SIZE = 64  # Adjust this size based on the maximum length in your dataset

# Convert hexadecimal ciphertext to a fixed-size numerical format
def hex_to_numeric(hex_str):
    byte_array = bytes.fromhex(hex_str)
    if len(byte_array) < FIXED_SIZE:
        byte_array = byte_array.ljust(FIXED_SIZE, b'\x00')  # Pad with zero bytes
    elif len(byte_array) > FIXED_SIZE:
        byte_array = byte_array[:FIXED_SIZE]  # Truncate
    return np.frombuffer(byte_array, dtype=np.uint8)

# Apply the conversion
df['ciphertext_numeric'] = df['ciphertext'].apply(hex_to_numeric)

# Prepare the data
X = np.array(list(df['ciphertext_numeric']))
y = df['algorithm'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
def train_rf_model():
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    joblib.dump(rf, 'stream_ciphers_rf_model.pkl')
    print(f'Random Forest Model Accuracy: {rf.score(X_test, y_test)}')

# Train the model
train_rf_model()
