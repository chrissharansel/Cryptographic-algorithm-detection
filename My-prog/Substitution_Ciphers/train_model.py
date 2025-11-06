import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load dataset with specific encoding (try different encodings if necessary)
try:
    df = pd.read_csv('substitution_ciphers_dataset.csv', encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv('substitution_ciphers_dataset.csv', encoding='ISO-8859-1')

# Preprocess data
# Convert each ciphertext string into its byte representation and create a list of those bytes
X = df['ciphertext'].apply(lambda x: list(x.encode())) 
# Ensure all entries are of the same length by padding them (assuming padding with 0 is acceptable)
max_len = max(X.apply(len))  # Find the max length of the ciphertext
X = X.apply(lambda x: x + [0]*(max_len - len(x)))  # Pad the shorter ciphertexts with zeros
X = np.array(X.tolist())  # Convert to a numpy array

# Target labels (algorithm used)
y = df['algorithm']

# Encode target labels (y) using LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Initialize and train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and label encoder using joblib
joblib.dump(model, 'substitution_ciphers_rf_model.pkl')
joblib.dump(label_encoder, 'substitution_ciphers_label_encoder.pkl')

print("Model and Label Encoder saved successfully!")
