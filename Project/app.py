from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_algorithm():
    # Get user input
    algorithm_type = request.form['algorithm']
    ciphertext = request.form['ciphertext']

    # Dummy Prediction: Always return AES
    predicted_algorithm = "AES"

    # Redirect to report page after prediction
    return redirect(url_for('report', predicted_algorithm=predicted_algorithm))

@app.route('/report/<predicted_algorithm>')
def report(predicted_algorithm):
    # Dummy security report for the predicted algorithm
    return render_template('report.html', algorithm=predicted_algorithm)

if __name__ == '__main__':
    app.run(debug=True)
