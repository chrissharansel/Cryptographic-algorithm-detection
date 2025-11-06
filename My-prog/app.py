from flask import Flask, request, jsonify, render_template
import subprocess
import os
app = Flask(__name__)

# Mapping the directories based on the type of algorithm
ALGORITHM_DIRS = {
    "block_ciphers": "Block_Cipher",
    "stream_ciphers": "Stream_Ciphers",
    "hash_functions": "Hash_Functions",
    "substitution_ciphers": "Substitution_Ciphers",
    "transposition_ciphers": "Transposition_Ciphers",
    "asymmetric_key_algorithms": "Asymmetric-Key_Algorithms_(Public-Key_Cryptography)",
    "key_exchange_algorithms": "Key_Exchange_Algorithms"
}

@app.route('/')
def index():
    # Serve the index.html file
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@app.route('/predict', methods=['POST'])
def predict_algorithm():
    data = request.get_json()
    algorithm_type = data['algorithmType']
    cipher_text = data['cipherText']

    # Define base directory and algorithm directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    algorithm_dir = os.path.join(base_dir, ALGORITHM_DIRS[algorithm_type])

    # Ensure the directory exists
    if not os.path.exists(algorithm_dir):
        os.makedirs(algorithm_dir)

    # Save cipher text into a temporary file for prediction
    input_file_path = os.path.join(algorithm_dir, "input_ciphertext.txt")
    with open(input_file_path, "w") as f:
        f.write(cipher_text)

    # Call the predict_data.py script for the selected algorithm
    try:
        result = subprocess.check_output(['python', os.path.join(algorithm_dir, 'predict_data.py')], universal_newlines=True)
        prediction = result.strip()
        return jsonify({"prediction": prediction})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)
