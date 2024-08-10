from flask import Flask, request, jsonify, render_template
import pandas as pd
import xgboost as xgb
import subprocess
import threading

app = Flask(__name__)

# Load the trained XGBoost model
model = xgb.Booster()
model.load_model('/root/fraud_detection/models/xgb_model.bin')

results = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_simulation', methods=['POST'])
def start_simulation():
    global results
    results = []
    thread = threading.Thread(target=run_simulation)
    thread.start()
    return jsonify({"status": "Simulation started"}), 200

def run_simulation():
    import time
    import requests

    data = pd.read_csv('/root/model_banking_system/app/simulation_dataset.csv')
    data = data.sample(frac=1).reset_index(drop=True)  # Shuffle the data

    for _, transaction in data.iterrows():
        transaction_data = {
            'step': transaction['step'],
            'customer': transaction['customer'],
            'age': transaction['age'],
            'gender': transaction['gender'],
            'merchant': transaction['merchant'],
            'category': transaction['category'],
            'amount': transaction['amount']
        }
        response = requests.post('http://localhost:5000/webhook', json=transaction_data)
        result = response.json()
        result['customer'] = transaction_data['customer']
        results.append(result)
        print(result)
        time.sleep(1)  # Adjust the delay as needed to simulate real-time transactions

@app.route('/simulation_results', methods=['GET'])
def simulation_results():
    return jsonify(results)

@app.route('/webhook', methods=['POST'])
def webhook_listener():
    transaction_data = request.json
    df = pd.DataFrame([transaction_data])

    categorical_features = ['customer', 'gender', 'merchant', 'category']
    for col in categorical_features:
        df[col] = pd.Categorical(df[col]).codes

    df = df[['step', 'customer', 'age', 'gender', 'merchant', 'category', 'amount']]
    dmatrix = xgb.DMatrix(df)
    prediction = model.predict(dmatrix)
    fraud_score = float(prediction[0])

    response = {
        'fraud_prediction': bool(fraud_score > 0.5),
        'fraud_score': fraud_score
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
