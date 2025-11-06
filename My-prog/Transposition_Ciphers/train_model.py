import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load dataset
df = pd.read_csv('transposition_ciphers_dataset.csv')

# Preprocess data
X = df['ciphertext'].apply(lambda x: list(x.encode()))
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
joblib.dump(model, 'rf_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
