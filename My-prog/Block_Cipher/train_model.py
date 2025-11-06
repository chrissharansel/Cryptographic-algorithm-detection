import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load dataset with a different encoding
try:
    df = pd.read_csv('block_ciphers_dataset.csv', encoding='latin1')
except UnicodeDecodeError:
    df = pd.read_csv('block_ciphers_dataset.csv', encoding='ISO-8859-1')

# Define maximum length for padding
MAX_LENGTH = 256

# Preprocess data
def preprocess_ciphertext(ciphertext, max_length=MAX_LENGTH):
    # Convert hex string back to bytes
    data_bytes = bytes.fromhex(ciphertext)
    # Convert bytes to numeric array and pad/truncate to max_length
    data_numeric = list(data_bytes)
    data_padded = data_numeric[:max_length] + [0] * (max_length - len(data_numeric))
    return data_padded

# Apply preprocessing
X = df['ciphertext'].apply(lambda x: preprocess_ciphertext(x))
X = np.array(X.tolist())
y = df['algorithm']

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save model and label encoder
joblib.dump(model, 'block_ciphers_rf_model.pkl')
joblib.dump(label_encoder, 'block_ciphers_label_encoder.pkl')
