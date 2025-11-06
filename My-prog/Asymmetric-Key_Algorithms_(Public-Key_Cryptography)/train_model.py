import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load dataset
df = pd.read_csv('asymmetric_key_algorithms_dataset.csv')

# Preprocess data - Convert ciphertext from hex to bytes and then to lists of integers
X = df['ciphertext'].apply(lambda x: list(bytes.fromhex(x)))

# Find the maximum length of feature vectors (ciphertexts)
max_len = max(X.apply(len))

# Function to pad sequences to the maximum length with zeros
def pad_sequences(seq, max_len):
    return seq + [0] * (max_len - len(seq))

# Apply padding to all feature vectors
X_padded = X.apply(lambda seq: pad_sequences(seq, max_len))

# Convert to a numpy array
X = np.array(X_padded.tolist())

# Encode the labels (algorithms)
y = df['algorithm']
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train a RandomForest model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Save the trained model and label encoder
joblib.dump(model, 'asymmetric_key_algorithms_rf_model.pkl')
joblib.dump(label_encoder, 'asymmetric_key_algorithms_label_encoder.pkl')

print("Model training completed and saved.")
